# -*- coding: utf-8 -*-
from copy import deepcopy

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

def checkType(var, type, T=None):
    """Check type."""
    if isinstance(var, type):
        if not T:
            return True
        if var.typeId == T:
            return True
    return False

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

    @property
    def typeId(self):
        return type(self.__data)
    
    def _update(self, data):
        self.setData(data['value'], True)

    def getData(self):
        return self.__data
    
    def setData(self, data, bit=False):
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
            if not bit:
                return
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

def updateForm(form, mode="update", options={}):
    # type: (CustomForm, str, dict) -> None
    if mode == 'sendMore':
        serverApi.GetSystem("SAPI", "world").NotifyToClient(
            form.id, 
            "%sCustomForm" % mode, 
            {
                "row": options['row'],
                "column": options['column']
            }
        )
        return
    data = []
    if not options:
        options = deepcopy(form._options)
    for key in ['resizable', 'movable', 'closable', 'pos', 'size', 'offset', 'margin']:
        if key not in options:
            continue
        if isinstance(options[key], (list, tuple)):
            i = 0
            for el in options[key]:
                options[key][i] = form._options[key][i].getData() if hasattr(form._options[key][i], "getData") else form._options[key][i]
                i += 1
        else:
            options[key] = options[key].getData() if hasattr(options[key], "getData") else options[key]
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
        elif control['type'] == 'dropdown':
            temp['label'] = control['label'].getData() if hasattr(control['label'], "getData") else control['label']
            temp['value'] = control['value'].getData() if hasattr(control['value'], "getData") else control['value']
            temp['items'] = control['items']
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
                options['style'] = "oreui"
            if "closable" not in options:
                options['closable'] = True
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
        if hasattr(options['resizable'], "getData"):
            CustomForms[self._formId]['obs'].append(options['resizable']._id)
        if hasattr(options['movable'], "getData"):
            CustomForms[self._formId]['obs'].append(options['movable']._id)
        if hasattr(options['closable'], "getData"):
            CustomForms[self._formId]['obs'].append(options['closable']._id)
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
                updateForm(self)

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
            {"formId": self._formId}
        )
        return self

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

    def dropdown(self, label, value, items, options={"visible": True}):
        # type: (str | Observable, Observable, list, dict) -> CustomForm
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
                "type": "dropdown",
                "label": label,
                "value": value,
                "items": items,
                "clientWritable": value._options['clientWritable'],
                "visible": options['visible'],
                "valueId": value._id
            }
        )
        if isinstance(label, Observable):
            CustomForms[self._formId]['obs'].append(label._id)
        CustomForms[self._formId]['obs'].append(value._id)
        if isinstance(options['visible'], Observable):
            CustomForms[self._formId]['obs'].append(options['visible']._id)
        updateForm(self)
        return self

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
        updateForm(self, "send")
        return self
    
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
    def create(player, title, options={"resizable": False, "movable": False, "style": "oreui", "closable": True}):
        # type: (__e.Player, str | Observable, dict) -> CustomForm
        return CustomForm(player, title, options)
    
class FormLayout:
    
    def __init__(self, layout={}):
        self.__position = layout.get("position", [0, 0])
        self.__offset = layout.get("offset", [0, 0])
        self.__size = layout.get("size", [1, 1])
        self.__margin = layout.get("margin", [0, 0, 0, 0])

    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            if len(value) > 1:
                if isinstance(value[0], (int, Observable)) and isinstance(value[1], (int, Observable)):
                    self.__position = [value[0], value[1]]
                else:
                    raise Exception("Set position failed! Elements must be int.")
            else:
                raise Exception("Set position failed! Position must has at least 2 elements.")
        else:
            raise Exception("Set position failed! Position must be a tuple or a list.")
    
    @property
    def offset(self):
        return self.__offset
    
    @offset.setter
    def offset(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            if len(value) > 1:
                if isinstance(value[0], (int, float, Observable)) and isinstance(value[1], (int, float, Observable)):
                    self.__offset = [value[0], value[1]]
                else:
                    raise Exception("Set offset failed! Elements must be float.")
            else:
                raise Exception("Set offset failed! Offset must has at least 2 elements.")
        else:
            raise Exception("Set offset failed! Offset must be a tuple or a list.")
    
    @property
    def size(self):
        return self.__size
    
    @size.setter
    def size(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            if len(value) > 1:
                if isinstance(value[0], (int, Observable)) and isinstance(value[1], (int, Observable)):
                    self.__size = [value[0], value[1]]
                else:
                    raise Exception("Set size failed! Elements must be int.")
            else:
                raise Exception("Set size failed! Size must has at least 2 elements.")
        else:
            raise Exception("Set size failed! Size must be a tuple or a list.")
    
    @property
    def margin(self):
        return self.__margin
    
    @margin.setter
    def margin(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            if len(value) > 3:
                if isinstance(value[0], (int, float, Observable)) and isinstance(value[1], (int, float, Observable)):
                    self.__margin = [value[0], value[1]]
                else:
                    raise Exception("Set margin failed! Elements must be float.")
            else:
                raise Exception("Set margin failed! Margin must has at least 2 elements.")
        else:
            raise Exception("Set margin failed! Margin must be a tuple or a list.")

class MoreUICustomData:

    def __init__(self, form, layout):
        # type: (CustomForm, FormLayout) -> None
        self.__form = form
        self.__layout = layout
    
    @property
    def form(self):
        return self.__form
    
    @property
    def layout(self):
        return self.__layout
    
class MoreUILayout:
    """
    Layout.
    """

    def __init__(self, layout={}):
        self.__row = layout.get("row", [1])
        self.__column = layout.get("column", [1])

    @property
    def row(self):
        return self.__row
    
    @row.setter
    def row(self, value):
        if isinstance(value, (list, tuple)):
            for el in value:
                if not isinstance(el, (float, int, Observable)):
                    raise TypeError("Property row excepted list[int | float], but got list[%s]" % type(el).__name__)
        else:
            raise TypeError("Property row excepted list[int | float], but got %s" % type(el).__name__)
        self.__row = value

    @property
    def column(self):
        return self.__column
    
    @column.setter
    def column(self, value):
        if isinstance(value, (list, tuple)):
            for el in value:
                if not isinstance(el, (float, int, Observable)):
                    raise TypeError("Property column excepted list[int | float], but got list[%s]" % type(el).__name__)
        else:
            raise TypeError("Property column excepted list[int | float], but got %s" % type(el).__name__)
        self.__column = value

class MoreUI:
    """
    A custom UI consisting of multiple forms.
    """
    _ID = 0

    import Entity as __e
    
    def __init__(self, player, layout={}):
        # type: (__e.Player, dict) -> None
        if not isinstance(player, self.__e.Player):
            raise Exception("Create MoreUI failed! arg 0 excepted type Player.")
        if not isinstance(layout, dict):
            raise Exception("Create MoreUI failed! arg 1 excepted type dict, but got type %s" % layout)
        self.__id = MoreUI._ID
        self.__forms = [] # type: list[MoreUICustomData]
        self.__layout = MoreUILayout(layout)
        if not isinstance(player, self.__e.Player):
            raise Exception("Create MoreUI failed! arg 0 excepted type <Player>, but got %s" % type(player).__name__)
        self.__player = player
        MoreUI._ID += 1

    @staticmethod
    def create(player, layout={}):
        # type: (__e.Player, dict) -> MoreUI
        """
        Create a MoreUI.
        """
        return MoreUI(player, layout)
    
    def addCustomForm(self, title, options={}, layout={}):
        if not isinstance(layout, dict):
            raise Exception("Add custom form failed! Arg 2 excepted dict, but got %s" % layout)
        fm = CustomForm.create(self.__player, title, options)
        data = MoreUICustomData(fm, FormLayout(layout))
        self.__forms.append(data)
        d = fm._options
        d['pos'] = data.layout.position
        d['size'] = data.layout.size
        d['offset'] = data.layout.offset
        d['margin'] = data.layout.margin
        for temp in [d['pos'], d['size'], d['offset'], d['margin']]:
            for el in temp:
                if hasattr(el, "getData"):
                    CustomForms[fm.formId]['obs'].append(el._id)
        updateForm(fm, "combine")
        return data
    
    @property
    def layout(self):
        """
        Layout of this UI.
        """
        return self.__layout

    @layout.setter
    def layout(self, style):
        if isinstance(style, dict):
            style = MoreUILayout(style)
        else:
            raise Exception("Set layout failed! style excepted type dict, but got %s" % type(style).__name__)
        self.__layout = style

    def addForm(self, form, layout={}):
        # type: (DynamicForm, dict) -> MoreUICustomData
        if not isinstance(form, CustomForm):
            raise Exception("Add form failed! Arg 0 excepted type <CustomForm>, but got %s" % type(form).__name__)
        if not isinstance(layout, dict):
            raise Exception("Add form failed! Arg 1 excepted type dict, but got %s" % type(layout).__name__)
        data = MoreUICustomData(form, FormLayout(layout))
        self.__forms.append(data)
        d = form._options
        d['pos'] = data.layout.position
        d['size'] = data.layout.size
        d['offset'] = data.layout.offset
        d['margin'] = data.layout.margin
        for temp in [d['pos'], d['size'], d['offset'], d['margin']]:
            for el in temp:
                if hasattr(el, "getData"):
                    CustomForms[form.formId]['obs'].append(el._id)
        updateForm(form, "combine")
        return data

    def show(self):
        # type: () -> None
        layout = {}
        layout['row'] = self.layout.row
        layout['column'] = self.layout.column
        updateForm(self.__player, "sendMore", layout)
        for formData in self.__forms:
            updateForm(formData.form, "combine")
