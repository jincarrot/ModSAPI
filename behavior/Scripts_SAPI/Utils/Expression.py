import math

class Old:

    def __init__(self):
        self.pow = math.pow
        self.sin = math.sin
        self.cos = math.cos

old = Old()

class New:

    def pow(self, x, y):
        if Expression and isinstance(x, Expression):
            return x._pow(y)
        elif Expression and isinstance(y, Expression):
            return Expression(x)._pow(y)
        else:
            return old.pow(x, y)
        
    def sin(self, x):
        if Expression and isinstance(x, Expression):
            return x._sin()
        else:
            return old.sin(x)
        
    def cos(self, x):
        if isinstance(x, Expression):
            return x._cos()
        else:
            return old.cos(x)

new = New()

math.pow = new.pow
math.sin = new.sin
math.cos = new.cos

class Expression(object):
    """表达式"""

    def __init__(self, value=0, op=None, next=0):
        # type: (float | Expression, float, Expression) -> None
        self.__value = value
        self.__operation = op
        self.__next = next

    @property
    def staticValue(self):
        # type: () -> float
        """获取静态值"""
        return float(self)

    def _change(self, value):
        self.__value = value

    def __str__(self):
        return str(float(self))

    def __int__(self):
        return int(float(self))
    
    def __float__(self):
        ori = float(self.__value)
        v = float(self.__next)
        if self.__operation == 1:
            ori += v
        elif self.__operation == 2:
            ori -= v
        elif self.__operation == 3:
            ori *= v
        elif self.__operation == 4:
            ori /= v
        elif self.__operation == 5:
            ori //= v
        elif self.__operation == 6:
            ori %= v
        elif self.__operation == 7:
            ori <<= v
        elif self.__operation == 8:
            ori >>=v
        elif self.__operation == 9:
            ori &= v
        elif self.__operation == 10:
            ori |= v
        elif self.__operation == 11:
            ori ^= v
        elif self.__operation == 12:
            ori = old.sin(ori)
        elif self.__operation == 13:
            ori = old.cos(ori)
        elif self.__operation == 14:
            ori = old.pow(ori, v)
        return ori
    
    def __add__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 1, value)
        return result
    
    def __radd__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 1, value)
        return result
    
    def __sub__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 2, value)
        return result

    def __rsub__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 2, value)
        return result

    def __mul__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 3, value)
        return result
    
    def __rmul__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 3, value)
        return result

    def __div__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 4, value)
        return result
    
    def __rdiv__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 4, value)
        return result
    
    def __floordiv__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 5, value)
        return result
    
    def __rfloordiv__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 5, value)
        return result
    
    def __mod__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 6, value)
        return result
    
    def __rmod__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 6, value)
        return result
    
    def __lshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 7, value)
        return result
    
    def __rlshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 7, value)
        return result
    
    def __rshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 8, value)
        return result
    
    def __rrshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 8, value)
        return result
    
    def __and__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 9, value)
        return result
    
    def __rand__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 9, value)
        return result
    
    def __or__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 10, value)
        return result
    
    def __ror__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 10, value)
        return result
    
    def __xor__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 11, value)
        return result
    
    def __rxor__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 11, value)
        return result
    
    def _sin(self):
        result = Expression(self, 12)
        return result
    
    def _cos(self):
        result = Expression(self, 13)
        return result
    
    def _pow(self, value):
        result = Expression(self, 14, value)
        return result
