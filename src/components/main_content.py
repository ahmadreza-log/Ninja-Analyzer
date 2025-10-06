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
            # Welcome header with gradient
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🎯 Welcome to Ninja Analyzer", 
                        size=32, 
                        weight=ft.FontWeight.BOLD, 
                        font_family="Iransans-Bold",
                        color=ft.Colors.CYAN_800
                    ),
                    ft.Text(
                        "Professional Website Analysis Tool", 
                        size=18, 
                        font_family="Iransans-Regular",
                        color=ft.Colors.GREY_600
                    ),
                    ft.Divider(height=20),
                    ft.Text(
                        "Select one of the analysis tools from the sidebar to begin analyzing your website's performance, SEO, and detecting potential issues.", 
                        size=16, 
                        font_family="Iransans-Regular",
                        color=ft.Colors.GREY_700
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE,
                padding=40,
                border_radius=ft.border_radius.all(15),
                border=ft.border.all(1, ft.Colors.CYAN_200),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.CYAN_100,
                    offset=ft.Offset(0, 2)
                )
            ),
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
        
        self.container = ft.Container(
            content=self.content_column,
            padding=ft.padding.all(30),
            expand=True,
            bgcolor=ft.Colors.GREY_50
        )
        
        return self.container
    
    def ShowSpeedAnalysis(self):
        """
        Shows the speed analysis page content.
        """
        speed_content = self.speed_analysis_page.CreateSpeedAnalysisPage()
        self.content_column.controls.clear()
        self.content_column.controls.append(speed_content)
        self.page.update()
    
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
        self.page.update()
    
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
        self.page.update()
