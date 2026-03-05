# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import random
import types

Observables = []
CustomForms = {} # type: dict[int, dict[str, list]]

class ActionFormData(object):
    """Builds a simple player form with buttons that let the player take action."""
    import Entity as en
    import FormResponse as fr

    def __init__(self):
        self.__title = ""
        self.__body = ""
        self.__button = []

    def title(self, titleText):
        # type: (str) -> ActionFormData
        """This builder method sets the title for the modal dialog."""
        self.__title = titleText
        return self
    
    def body(self, bodyText):
        # type: (str) -> ActionFormData
        """Method that sets the body text for the modal form."""
        self.__body = bodyText
        return self
    
    def button(self, text, icon=None):
        # type: (str, str) -> None
        """Adds a button to this form with an icon from a resource pack."""
        self.__button.append([text, icon])
        return self
    
    def show(self, player):
        # type: (en.Player) -> fr.Promise
        """Creates and shows this modal popup form. Returns asynchronously when the player confirms or cancels the dialog."""
        id = random.randint(0, 32767)
        serverApi.GetSystem("SAPI", "world").NotifyToClient(player.id, "showActionForm", {"formId": id, "title": self.__title, "body": self.__body, "button": self.__button})
        return self.fr.Promise(id)

class ModalFormData(object):
    """Used to create a fully customizable pop-up form for a player."""
    import Entity as en
    import FormResponse as fr

    def __init__(self):
        self.__title = ""
        self.__elements = []

    def title(self, titleText):
        # type: (str) -> ModalFormData
        """This builder method sets the title for the modal dialog."""
        self.__title = titleText
        return self
    
    def toggle(self, label, defaultValue=False):
        # type: (str, bool) -> ModalFormData
        """Adds a toggle checkbox button to the form."""
        data = {
            "type": "toggle",
            "label": label
        }
        self.__elements.append(data)
        return self
    
    def title(self, titleText):
        # type: (str) -> None
        """This builder method sets the title for the modal dialog."""
        self.__title = titleText
        return self
    
    def textField(self, label, placeholderText, defaultValue=""):
        # type: (str, str, str) -> ModalFormData
        """Adds a textbox to the form."""
        data = {
            "type": "input",
            "label": label
        }
        self.__elements.append(data)
        return self
    
    def slider(self, label, mininumValue, maxinumValue, valueStep, defaultValue=0):
        # type: (str, int, int, int, int) -> ModalFormData
        """Adds a numeric slider to the form."""
        data = {
            "type": "step_slider",
            "label": label
        }
        self.__elements.append(data)
        return self
    
    def show(self, player):
        # type: (en.Player) -> fr.Promise
        """Creates and shows this modal popup form. Returns asynchronously when the player confirms or cancels the dialog."""
        id = random.randint(0, 32767)
        serverApi.GetSystem("SAPI", "world").NotifyToClient(player.id, "showModalForm", {"formId": id, "title": self.__title, "elements": self.__elements})
        return self.fr.Promise(id)

class Observable:
    """
    A class that represents data that can be Observed. Extensively used for UI.
    """
    ID = 0

    def __init__(self, data, options):
        if type(options) == dict:
            if "clientWritable" not in options:
                options['clientWritable'] = False
        else:
            raise TypeError("Create observable failed! Options should be a dict, but got %s" % type(options).__name__)
        if type(data) in [int, float, str, bool]:
            self.__data = data
            self.__callbacks = []
            self._options = options
            self._id = Observable.ID
            Observable.ID += 1

            if options['clientWritable']:
                serverApi.GetSystem("SAPI", "world").ListenForEvent("SAPI", "SAPI_C", "updateObservable%s" % self._id, self, self._update)
        else:
            raise TypeError("Create observable failed! Expected type int | float | str | bool, but got %s" % (type(self.__data).__name__, type(data).__name__))

    def _update(self, data):
        self.setData(data['value'])

    def getData(self):
        return self.__data
    
    def setData(self, data):
        # Inner type conversation.
        if data == self.__data:
            return
        if type(self.__data) == str:
            data = str(data)
        elif type(self.__data) == bool:
            data = bool(data)
        if type(data) == int and type(self.__data) == float:
            data = float(data)
        if type(data) == float and type(self.__data) == int:
            data = int(data)
        # Set data or throw error.
        if type(data) == type(self.__data):
            self.__data = data
            for callback in self.__callbacks:
                callback(self.__data)
            for formId in CustomForms:
                if self._id in CustomForms[formId]['obs']:
                    updateForm(CustomForms[formId]['form'])
        else:
            raise TypeError("Observable expected data of type %s, but got %s" % (type(self.__data).__name__, type(data).__name__))
        
    def subscribe(self, callback):
        # type: (types.FunctionType) -> None
        if callback not in self.__callbacks:
            self.__callbacks.append(callback)
    
    def unsubscribe(self, callback):
        # type: (types.FunctionType) -> None
        if callback in self.__callbacks:
            self.__callbacks.remove(callback)

    @staticmethod
    def create(data, options={"clientWritable": False}):
        ob = Observable(data, options)
        Observables.append(ob)
        return ob

def updateForm(form, mode="update", options=None):
    # type: (CustomForm, str, dict) -> None
    data = []
    for control in form._data:
        temp = {"type": control['type']}
        # Generate data.
        if control['type'] == 'button':
            temp["label"] = control['label'].getData() if hasattr(control['label'], "getData") else control['label']
        elif control['type'] == 'label':
            temp["text"] = control['text'].getData() if hasattr(control['text'], "getData") else control['text']
        elif control['type'] == 'textField':
            temp['label'] = control['label'].getData() if hasattr(control['label'], "getData") else control['label']
            temp['text'] = control['text'].getData() if hasattr(control['text'], "getData") else control['text']
            temp['clientWritable'] = control['clientWritable']
            temp['textId'] = control['textId']
        elif control['type'] == 'toggle':
            temp['label'] = control['label'].getData() if hasattr(control['label'], "getData") else control['label']
            temp['toggled'] = control['toggled'].getData() if hasattr(control['toggled'], "getData") else control['toggled']
            temp['clientWritable'] = control['clientWritable']
            temp['toggledId'] = control['toggledId']
        elif control['type'] == 'slider':
            temp['label'] = control['label'].getData() if hasattr(control['label'], "getData") else control['label']
            temp['value'] = control['value'].getData() if hasattr(control['value'], "getData") else control['value']
            temp['minValue'] = control['minValue'].getData() if hasattr(control['minValue'], "getData") else control['minValue']
            temp['maxValue'] = control['maxValue'].getData() if hasattr(control['maxValue'], "getData") else control['maxValue']
            temp['clientWritable'] = control['clientWritable']
            temp['valueId'] = control['valueId']
        temp['visible'] = control['visible'].getData() if hasattr(control['visible'], "getData") else control['visible']
        data.append(temp)
    serverApi.GetSystem("SAPI", "world").NotifyToClient(
            form._player.id, 
            "%sCustomForm" % mode, 
            {
                "formId": form._formId,
                "title": form._title.getData() if hasattr(form._title, "getData") else form._title,
                "data": data,
                "options": options
            }
        )

class DynamicForm:
    """Base class of dynamic forms (CustomForm, MessageForm)."""
    pass

class CustomForm(DynamicForm):
    """
    A customizable form that lets you put buttons, labels, toggles, dropdowns, sliders, and more into a form! 
    Built on top of Observable, the form will update when the Observables' value changes.
    """
    ID = 0
    import Entity as __e

    def __init__(self, player, title, options):
        # type: (__e.Player, str | Observable, dict) -> None
        # Type checking.
        if not isinstance(player, self.__e.Player):
            raise Exception("Create custom form failed! arg 0 excepted type Player")
        if not type(title.getData() if hasattr(title, "getData") else title) == str:
            raise Exception(
                "Create custom form failed! arg 1 excepted type str | Observable<str>, but got %s" % (
                    (
                        "Observable<%s>" % type(title.getData()).__name__
                    ) if hasattr(title, "getData") 
                    else type(title).__name__
                )
            )
        if not isinstance(options, dict):
            raise Exception(
                "Custom form create failed! arg 2 expected type dict, but got %s" % type(options).__name__
            )
        else:
            if "resizable" not in options:
                options['resizable'] = False
            if "movable" not in options:
                options['movable'] = False
            if "style" not in options:
                options['movable'] = "oreui"
        # Set data.
        self._player = player
        self._title = title
        self._data = []
        self._options = options
        self._formId = CustomForm.ID
        CustomForm.ID += 1
        CustomForms[self._formId] = {
            "form": self,
            "obs": []
        }
        if hasattr(title, "getData"):
            CustomForms[self._formId]['obs'].append(title._id)
        
        serverApi.GetSystem("SAPI", "world").ListenForEvent("SAPI", "SAPI_C", "updateForm%s" % self._formId, self, self._update)

    @property
    def formId(self):
        return self._formId
    
    def _update(self, data):
        selection = data['selection']
        index = 0
        selected = None
        for controlData in self._data:
            if not controlData['visible']:
                continue
            if index == selection:
                selected = controlData
                break
            index += 1
        if data['operation'] == 'buttonClick':
            if 'callback' in selected:
                selected['callback']()

    def button(self, label, onClick, options={"visible": True}):
        # type: (str | Observable, types.FunctionType, dict) -> CustomForm
        # Type checking.
        label_value = label.getData() if hasattr(label, "getData") else label
        if not isinstance(label_value, str):
            if hasattr(label, "getData"):
                actual_type = "Observable<%s>" % type(label.getData()).__name__
            else:
                actual_type = type(label).__name__
            raise Exception(
                "CustomForm create button failed! arg 0 expected type str | Observable<str>, but got %s" % actual_type
            )
        if not isinstance(options, dict):
            raise Exception(
                "CustomForm create button failed! arg 1 expected type dict, but got %s" % type(options).__name__
            )
        else:
            if "visible" not in options:
                options['visible'] = True
        # Data store.
        self._data.append(
            {
                "type": "button",
                "label": label,
                "callback": onClick,
                "visible": options['visible']
            }
        )
        if isinstance(label, Observable):
            CustomForms[self._formId]['obs'].append(label._id)
        if isinstance(options['visible'], Observable):
            CustomForms[self._formId]['obs'].append(options['visible']._id)
        updateForm(self)
        return self
    
    def close(self):
        serverApi.GetSystem("SAPI", "world").NotifyToClient(
            self._player.id, 
            "closeCustomForm", 
            {}
        )

    def divider(self, options={"visible": True}):
        # type: (dict) -> CustomForm
        # Type checking.
        if not isinstance(options, dict):
            raise Exception(
                "CustomForm create button failed! arg 1 expected type dict, but got %s" % type(options).__name__
            )
        else:
            if "visible" not in options:
                options['visible'] = True
        # Data store.
        self._data.append(
            {
                "type": "divider",
                "visible": options['visible']
            }
        )
        if isinstance(options['visible'], Observable):
            CustomForms[self._formId]['obs'].append(options['visible']._id)
        updateForm(self)
        return self

    def _dropdown(self, label, value, items, options={"visible": True}):
        pass

    def label(self, text, options={"visible": True}):
        # type: (str | Observable, dict) -> CustomForm
        # Type checking.
        label_value = text.getData() if hasattr(text, "getData") else text
        if not isinstance(label_value, str):
            if hasattr(text, "getData"):
                actual_type = "Observable<%s>" % type(text.getData()).__name__
            else:
                actual_type = type(text).__name__
            raise Exception(
                "CustomForm create button failed! arg 0 expected type str | Observable<str>, but got %s" % actual_type
            )
        if not isinstance(options, dict):
            raise Exception(
                "CustomForm create button failed! arg 1 expected type dict, but got %s" % type(options).__name__
            )
        else:
            if "visible" not in options:
                options['visible'] = True
        # Data store.
        self._data.append(
            {
                "type": "label",
                "text": text,
                "visible": options['visible']
            }
        )
        if isinstance(text, Observable):
            CustomForms[self._formId]['obs'].append(text._id)
        if isinstance(options['visible'], Observable):
            CustomForms[self._formId]['obs'].append(options['visible']._id)
        updateForm(self)
        return self

    def show(self):
        updateForm(self, "send", self._options)
    
    def slider(self, label, value, minValue, maxValue, options={"visible": True}):
        # type: (str | Observable, Observable, int | Observable, int | Observable, dict) -> CustomForm
        # Type checking.
        label_value = label.getData() if hasattr(label, "getData") else label
        if not isinstance(label_value, str):
            if hasattr(label, "getData"):
                actual_type = "Observable<%s>" % type(label.getData()).__name__
            else:
                actual_type = type(label).__name__
            raise Exception(
                "CustomForm create button failed! arg 0 expected type str | Observable<str>, but got %s" % actual_type
            )
        if not isinstance(value, Observable):
            raise Exception(
                "CustomForm create button failed! arg 1 expected type Observable<int>, but got %s" % type(toggled).__name__
            )
        else:
            if not value._options['clientWritable']:
                raise Exception("Excepted value observable to be client writable.")
            if type(value.getData()) not in [int, float]:
                raise Exception(
                    "CustomForm create button failed! arg 1 expected type Observable<int>, but got Observable<%s>" % type(value.getData()).__name__
                )
        min_value = minValue.getData() if hasattr(minValue, "getData") else minValue
        if not isinstance(min_value, int):
            if hasattr(minValue, "getData"):
                actual_type = "Observable<%s>" % type(minValue.getData()).__name__
            else:
                actual_type = type(minValue).__name__
            raise Exception(
                "CustomForm create button failed! arg 0 expected type int | Observable<int>, but got %s" % actual_type
            )
        max_value = maxValue.getData() if hasattr(maxValue, "getData") else maxValue
        if not isinstance(max_value, int):
            if hasattr(maxValue, "getData"):
                actual_type = "Observable<%s>" % type(maxValue.getData()).__name__
            else:
                actual_type = type(maxValue).__name__
            raise Exception(
                "CustomForm create button failed! arg 0 expected type int | Observable<int>, but got %s" % actual_type
            )
        if not isinstance(options, dict):
            raise Exception(
                "CustomForm create button failed! arg 2 expected type dict, but got %s" % type(options).__name__
            )
        else:
            if "visible" not in options:
                options['visible'] = True
        # Data store.
        self._data.append(
            {
                "type": "slider",
                "label": label,
                "value": value,
                "minValue": minValue,
                "maxValue": maxValue,
                "clientWritable": value._options['clientWritable'],
                "visible": options['visible'],
                "valueId": value._id
            }
        )
        if isinstance(label, Observable):
            CustomForms[self._formId]['obs'].append(label._id)
        CustomForms[self._formId]['obs'].append(value._id)
        if isinstance(minValue, Observable):
            CustomForms[self._formId]['obs'].append(minValue._id)
        if isinstance(maxValue, Observable):
            CustomForms[self._formId]['obs'].append(maxValue._id)
        if isinstance(options['visible'], Observable):
            CustomForms[self._formId]['obs'].append(options['visible']._id)
        updateForm(self)
        return self

    def spacer(self, options={"visible": True}):
        return self.label("", options)

    def textField(self, label, text, options={"visible": True}):
        # type: (str | Observable, Observable, dict) -> CustomForm
        # Type checking.
        label_value = label.getData() if hasattr(label, "getData") else label
        if not isinstance(label_value, str):
            if hasattr(label, "getData"):
                actual_type = "Observable<%s>" % type(label.getData()).__name__
            else:
                actual_type = type(label).__name__
            raise Exception(
                "CustomForm create button failed! arg 0 expected type str | Observable<str>, but got %s" % actual_type
            )
        if not isinstance(text, Observable):
            raise Exception(
                "CustomForm create button failed! arg 1 expected type Observable<str>, but got %s" % type(text).__name__
            )
        else:
            if not text._options['clientWritable']:
                raise Exception("Excepted text observable to be client writable.")
            if not type(text.getData()) == str:
                raise Exception(
                    "CustomForm create button failed! arg 1 expected type Observable<str>, but got Observable<%s>" % type(text.getData()).__name__
                )
        if not isinstance(options, dict):
            raise Exception(
                "CustomForm create button failed! arg 2 expected type dict, but got %s" % type(options).__name__
            )
        else:
            if "visible" not in options:
                options['visible'] = True
        # Data store.
        self._data.append(
            {
                "type": "textField",
                "label": label,
                "text": text,
                "clientWritable": text._options['clientWritable'],
                "textId": text._id,
                "visible": options['visible']
            }
        )
        if isinstance(label, Observable):
            CustomForms[self._formId]['obs'].append(label._id)
        CustomForms[self._formId]['obs'].append(text._id)
        if isinstance(options['visible'], Observable):
            CustomForms[self._formId]['obs'].append(options['visible']._id)
        updateForm(self)
        return self

    def toggle(self, label, toggled, options={"visible": True}):
        # type: (str | Observable, Observable, dict) -> CustomForm
        # Type checking.
        label_value = label.getData() if hasattr(label, "getData") else label
        if not isinstance(label_value, str):
            if hasattr(label, "getData"):
                actual_type = "Observable<%s>" % type(label.getData()).__name__
            else:
                actual_type = type(label).__name__
            raise Exception(
                "CustomForm create button failed! arg 0 expected type str | Observable<str>, but got %s" % actual_type
            )
        if not isinstance(toggled, Observable):
            raise Exception(
                "CustomForm create button failed! arg 1 expected type Observable<bool>, but got %s" % type(toggled).__name__
            )
        else:
            if not toggled._options['clientWritable']:
                raise Exception("Excepted text observable to be client writable.")
            if not type(toggled.getData()) == bool:
                raise Exception(
                    "CustomForm create button failed! arg 1 expected type Observable<bool>, but got Observable<%s>" % type(toggled.getData()).__name__
                )
        if not isinstance(options, dict):
            raise Exception(
                "CustomForm create button failed! arg 2 expected type dict, but got %s" % type(options).__name__
            )
        else:
            if "visible" not in options:
                options['visible'] = True
        # Data store.
        self._data.append(
            {
                "type": "toggle",
                "label": label,
                "toggled": toggled,
                "clientWritable": toggled._options['clientWritable'],
                "visible": options['visible'],
                "toggledId": toggled._id
            }
        )
        if isinstance(label, Observable):
            CustomForms[self._formId]['obs'].append(label._id)
        CustomForms[self._formId]['obs'].append(toggled._id)
        if isinstance(options['visible'], Observable):
            CustomForms[self._formId]['obs'].append(options['visible']._id)
        updateForm(self)
        return self
        
    @staticmethod
    def create(player, title, options={"resizable": False, "movable": False, "style": "oreui"}):
        # type: (__e.Player, str | Observable, dict) -> CustomForm
        return CustomForm(player, title, options)
    
class Layout:

    def __init__(self):
        self.__row = []
        self.__column = []

    @property
    def row(self):
        return self.__row

    @property
    def column(self):
        return self.__column

    @staticmethod
    def create():
        return Layout()

class MoreUI:
    """
    A custom UI consisting of multiple forms.
    """
    _ID = 0
    
    def __init__(self):
        self.__id = MoreUI._ID
        self.__forms = []
        self.__layout = {}
        MoreUI._ID += 1

    @staticmethod
    def create():
        # type: () -> MoreUI
        """
        Create a MoreUI.
        """
        return MoreUI()
    
    def addCustomForm(self, player, title, options={"resizable": False, "movable": False, "style": "oreui"}):
        fm = CustomForm.create(player, title, options)
        self.__forms.append(fm)
        return fm
    
    @property
    def layout(self):
        # type: () -> list[str | int | float]
        """
        Layout of this UI.
        """
        pass

    @layout.setter
    def layout(self, style):
        pass

    def addForm(self, form):
        # type: (DynamicForm) -> None
        pass

    def show(self):
        # type: () -> None
        for form in self.__forms:
            updateForm(form, "combine")
