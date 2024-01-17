import re
from collections import namedtuple


RGB = namedtuple("RGB", ["red", "green", "blue"])


def rgb_contrast(color1: RGB, color2: RGB) -> float:
    """
    Calculates the contrast ratio between two RGB values (tuple of RGB in 0.0 - 1.0 range)
    """
    for color in (color1, color2):
        if not 0.0 <= color.red <= 1.0:
            raise ValueError("red is out of valid range (0.0 - 1.0)")
        if not 0.0 <= color.green <= 1.0:
            raise ValueError("green is out of valid range (0.0 - 1.0)")
        if not 0.0 <= color.blue <= 1.0:
            raise ValueError("blue is out of valid range (0.0 - 1.0)")

    l1 = _relative_luminance(color1)
    l2 = _relative_luminance(color2)

    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)


def hex_contrast(color1: str, color2: str) -> float:
    """
    Calculates the contrast ratio between two colors expressed in hex values (eg #FFFFFF and #000000)
    """
    rgb1 = _hex_to_rgb(color1)
    rgb2 = _hex_to_rgb(color2)
    contrast_ratio = rgb_contrast(rgb1, rgb2)

    return contrast_ratio


def passes(hex1: str, hex2: str, level: str = "AA", large: bool = False) -> bool:
    """
    Checks if a given color has a contrast ratio as required by WCAG for "AA" or "AAA" levels.

    Args:
        hex1 (str): The first color in hexadecimal format.
        hex2 (str): The second color in hexadecimal format.
        level (str, optional): The contrast level to check ("AA" or "AAA"). Defaults to "AA".
        large (bool, optional): Whether the text is large or not. Defaults to False.

    Returns:
        bool: True if the contrast ratio meets the requirements, False otherwise.

    Raises:
        ValueError: If an invalid contrast level is provided.
    """
    contrast_ratio = hex_contrast(hex1, hex2)
    match level:
        case "AA":
            if large:
                return contrast_ratio >= 3.0
            else:
                return contrast_ratio >= 4.5
        case "AAA":
            if large:
                return contrast_ratio >= 4.5
            else:
                return contrast_ratio >= 7.0
        case _:
            raise ValueError("Invalid contrast level. Must be 'AA' (default) or 'AAA'")


def _hex_to_rgb(hex_value: str) -> RGB:
    """
    Convert a hexadecimal color code to its RGB representation.

    Args:
        hex_value (str): The hexadecimal color code to convert example: "#FF0000".

    Returns:
        A tuple representing the RGB values of the color, each value ranging from 0 to 1.

    Raises:
        ValueError: If the input hex_value is not a valid hexadecimal color code.

    Example:
        >>> _hex_to_rgb("#FF0000")
        RGB(red=1.0, green=0.0, blue=0.0)
    """

    if not isinstance(hex_value, str):
        raise ValueError(f"Invalid hex value {hex_value}")

    if not re.match(r"^#([A-Fa-f0-9]{6})$", hex_value):
        raise ValueError(f"Invalid hex value {hex_value}")

    hex_value = hex_value.lstrip("#")
    return RGB(
        int(hex_value[0:2], base=16) / 255,
        int(hex_value[2:4], base=16) / 255,
        int(hex_value[4:6], base=16) / 255,
    )


def _relative_luminance(color: RGB) -> float:
    """
    Calculate the relative luminance of a color based on its RGB values.

    Args:
        color (RGB): The color to calculate the relative luminance of.

    Returns:
        The relative luminance of the color.
    """
    red = _linearize(color.red)
    green = _linearize(color.green)
    blue = _linearize(color.blue)

    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _linearize(value: float) -> float:
    """
    Linearizes a given value according to the sRGB color space specification.

    Parameters:
        value (float): The value to be linearized.

    Returns:
        float: The linearized value.

    Description:
        This function takes a value and linearizes it based on the sRGB color space specification.
        The linearization process involves checking if the value is less than or equal to 0.03928.
        If it is, the value is divided by 12.92. Otherwise, the value is adjusted by adding 0.055,
        dividing by 1.055, and raising it to the power of 2.4.

    Note:
        The sRGB color space is a standardized RGB color space that is widely used in various applications
        such as image editing, web design, and digital displays. It provides a consistent and perceptually
        uniform representation of colors across different devices and platforms.
    """
    if value <= 0.03928:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4
