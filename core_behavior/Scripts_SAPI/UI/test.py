from Controls import *

def a():
    xxx = 0
    return Label(xxx)

controlA = [
    Label(),
    Panel() <= [
        # child controls
        Button(),
        Label()
    ],
    Panel() <= [
        a,
        Label("hello")
    ]
]
