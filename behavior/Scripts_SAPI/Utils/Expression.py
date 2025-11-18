import math

class Old:

    def __init__(self):
        self.pow = math.pow
        self.sin = math.sin
        self.cos = math.cos
        self.max = max
        self.min = min
        self.abs = abs

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
        
    def max(self, *args):
        # type: (Expression) -> None
        isExpression = False
        for value in args:
            if isinstance(value, Expression):
                isExpression = True
                break
        if isExpression:
            v = Expression(0, 15, args)
            return v if len(args) > 1 else Expression(args[0])
        else:
            return old.max(args) if len(args) > 1 else args[0]
        
    def min(self, *args):
        # type: (Expression) -> None
        isExpression = False
        for value in args:
            if isinstance(value, Expression):
                isExpression = True
                break
        if isExpression:
            v = Expression(0, 16, args)
            return v if len(args) > 1 else Expression(args[0])
        else:
            return old.min(args) if len(args) > 1 else args[0]

    def sqrt(self, x):
        return self.pow(x, 0.5)

    def abs(self, x):
        if Expression and isinstance(x, Expression):
            return x._abs()
        else:
            return old.abs(x)

new = New()

math.pow = new.pow
math.sin = new.sin
math.cos = new.cos
math.sqrt = new.sqrt
max = new.max
min = new.min
abs = new.abs

class Expression(object):
    """表达式"""

    def __init__(self, value=0, op=None, next=0):
        # type: (float | Expression, int, Expression) -> None
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
        v = float(self.__next if (type(self.__next) in [int, float] or isinstance(self.__next, Expression)) else 0)
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
        elif self.__operation == 15:
            ori = old.max(self.__next)
        elif self.__operation == 16:
            ori = old.min(self.__next)
        elif self.__operation == 17:
            ori = old.abs(ori)
        return ori
    
    def __add__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 1, value)
        return result
    
    def __radd__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 1, self)
        return result
    
    def __sub__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 2, value)
        return result

    def __rsub__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 2, self)
        return result

    def __mul__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 3, value)
        return result
    
    def __rmul__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 3, self)
        return result

    def __div__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 4, value)
        return result
    
    def __rdiv__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 4, self)
        return result
    
    def __floordiv__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 5, value)
        return result
    
    def __rfloordiv__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 5, self)
        return result
    
    def __mod__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 6, value)
        return result
    
    def __rmod__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 6, self)
        return result
    
    def __lshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 7, value)
        return result
    
    def __rlshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 7, self)
        return result
    
    def __rshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 8, value)
        return result
    
    def __rrshift__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 8, self)
        return result
    
    def __and__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 9, value)
        return result
    
    def __rand__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 9, self)
        return result
    
    def __or__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 10, value)
        return result
    
    def __ror__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 10, self)
        return result
    
    def __xor__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(self, 11, value)
        return result
    
    def __rxor__(self, value):
        # type: (float | Expression) -> Expression
        result = Expression(value, 11, self)
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
    
    def _abs(self):
        result = Expression(self, 17)
        return result
