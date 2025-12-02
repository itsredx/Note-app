# constants.colors.py
from pythra import Colors
from .theme import theme
from dataclasses import dataclass


@dataclass
class AppColors:
    appBackgroundColorDarkMode = Colors.hex("#2c2c2c") #1C1C1C
    appBackgroundColorLightMode = Colors.white

    iconDarkMode = Colors.hex("#d3d3d3") #e2a5a3
    iconLightMode = Colors.black  # hex("#262626")

    iconLightModeFormatColorTextRounded = Colors.GREY

    buttonDarkBackgroundColor = Colors.hex("#4c4c4c") #837b7b #383838
    buttonLightBackgroundColor = Colors.hex("#e9ecef")

    buttonDarkHoverColor = Colors.hex("#383838")
    buttonDarkActiveColor = Colors.rgba(211, 211, 211, 0.50)
    buttonLightHoverColor = Colors.rgba(0, 0, 0, 0.20) #0.08

    dropDownDarkHoverColor = buttonDarkHoverColor
    dropDownItemDarkHoverColor = Colors.rgba(103, 80, 164, 0.37)

    dropDownMenuDarkHoverColor = Colors.hex("#4c4c4c")
    dropDownMenuLightHoverColor = Colors.hex("#e9ecef")

    dropDownDarkColor = Colors.hex("#4c4c4c")
    dropDownLightColor = Colors.hex("#e9ecef")

    toolbarBackgroundDarkColor = Colors.hex("#2c2c2c")

    transparent = Colors.transparent