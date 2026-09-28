from nyuGUI.core import Dim, Root, Widget
from nyuGUI.widgets import Button, TextLabel

app = Root(title="Weird Configuration App", bgcolor = "#0D1B2A")
page_tab = Widget(
    height = Dim(1, 0),
    width = Dim(0, 270),
    bgcolor = "#1B263B",
    parent = app,
)

device_information_button = Button(
    parent = page_tab,
    width = Dim(1, 0),
    height = Dim(0.15, 0),
    text = "Device Information",
    bgcolor = "#415A77",
    hover_bgcolor = "#778DA9",
    pressed_bgcolor = "#FFFFFF",
    font_size = 30,
)

app.run()
