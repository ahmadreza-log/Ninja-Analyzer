"""
Main content component for the Ninja Analyzer application.
This module handles the main content area and page switching functionality.
"""

import flet as ft
from src.pages.speed_analysis import SpeedAnalysisPage

class MainContentComponent:
    """
    Main content component class that handles the main content area.
    """
    
    def __init__(self):
        """Initialize the main content component."""
        self.container = None
        self.content_column = None
        self.speed_analysis_page = SpeedAnalysisPage()
        self.page = None
        
    def CreateMainContent(self, page):
        """
        Creates and returns the main content container.
        
        Args:
            page (ft.Page): The Flet page object
            
        Returns:
            ft.Container: The main content container
        """
        self.page = page
        self.speed_analysis_page.set_page(page)
        
        self.content_column = ft.Column([
            ft.Text(
                "Welcome to Ninja Analyzer", 
                size=24, 
                weight=ft.FontWeight.BOLD, 
                font_family="Iransans-Bold"
            ),
            ft.Text(
                "Select one of the sidebar options to get started.", 
                size=16, 
                font_family="Iransans-Regular"
            ),
        ], scroll=ft.ScrollMode.AUTO)
        
        self.container = ft.Container(
            content=self.content_column,
            padding=ft.padding.only(left=20),
            expand=True
        )
        
        return self.container
    
    def ShowSpeedAnalysis(self):
        """
        Shows the speed analysis page content.
        """
        speed_content = self.speed_analysis_page.CreateSpeedAnalysisPage()
        self.content_column.controls.clear()
        self.content_column.controls.append(speed_content)
    
    def ShowSeoAnalysis(self):
        """
        Shows the SEO analysis page content.
        """
        self.content_column.controls.clear()
        self.content_column.controls.append(
            ft.Text(
                "SEO Analysis Page", 
                size=24, 
                weight=ft.FontWeight.BOLD, 
                font_family="Iransans-Bold"
            )
        )
        self.content_column.controls.append(
            ft.Text(
                "This section is designed for website SEO analysis.", 
                size=16, 
                font_family="Iransans-Regular"
            )
        )
    
    def ShowBugAnalysis(self):
        """
        Shows the bug analysis page content.
        """
        self.content_column.controls.clear()
        self.content_column.controls.append(
            ft.Text(
                "Bug Detection Page", 
                size=24, 
                weight=ft.FontWeight.BOLD, 
                font_family="Iransans-Bold"
            )
        )
        self.content_column.controls.append(
            ft.Text(
                "This section is designed for website bug detection.", 
                size=16, 
                font_family="Iransans-Regular"
            )
        )
