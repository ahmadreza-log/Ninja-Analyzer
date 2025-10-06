"""
Font configuration for the Ninja Analyzer application.
This module handles all font-related settings and font family definitions.
"""

import flet as ft

def GetFontConfig():
    """
    Returns the font configuration for the application.
    
    Returns:
        dict: Dictionary containing font configurations
    """
    return {
        "Iransans-Regular": "fonts/Iransans-Regular.ttf",
        "Iransans-Bold": "fonts/Iransans-Bold.ttf",
        "Iransans-Medium": "fonts/Iransans-Medium.ttf",
        "Iransans-Light": "fonts/Iransans-Light.ttf",
        "Iransans-Ultralight": "fonts/Iransans-Ultralight.ttf",
        "Iransans-Black": "fonts/Iransans-Black.ttf"
    }

def ApplyFontTheme(page: ft.Page):
    """
    Applies the font theme to the page.
    
    Args:
        page (ft.Page): The Flet page object
    """
    page.fonts = GetFontConfig()
    page.theme = ft.Theme(font_family="Iransans-Regular")
    # Set text direction to left-to-right for English interface
    page.theme.text_theme = ft.TextTheme()
