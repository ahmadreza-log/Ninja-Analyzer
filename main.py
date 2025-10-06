"""
Ninja Analyzer - Website Analysis Tool
Main application file that orchestrates all components.

This application provides website analysis capabilities including:
- Speed analysis
- SEO analysis  
- Bug detection
"""

import flet as ft
from src.config.fonts import ApplyFontTheme
from src.components.sidebar import SidebarComponent
from src.components.main_content import MainContentComponent

class NinjaAnalyzerApp:
    """
    Main application class for the Ninja Analyzer.
    Handles the overall application structure and component coordination.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.page = None
        self.sidebar_component = None
        self.main_content_component = None
        
    def SetupPage(self, page: ft.Page):
        """
        Setup the main page with all configurations.
        
        Args:
            page (ft.Page): The Flet page object
        """
        self.page = page
        page.title = "Website Analyzer - Ninja Analyzer"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = False
        page.padding = 20
        page.rtl = False
        
        # Apply font configuration
        ApplyFontTheme(page)
        
        # Initialize components
        self.main_content_component = MainContentComponent()
        self.sidebar_component = SidebarComponent(
            on_speed_click=self.OnSpeedAnalysisClick,
            on_seo_click=self.OnSeoAnalysisClick,
            on_bug_click=self.OnBugAnalysisClick
        )
        
        # Create and add components to page
        self.CreateLayout()
    
    def CreateLayout(self):
        """Create the main application layout."""
        sidebar = self.sidebar_component.CreateSidebar()
        main_content = self.main_content_component.CreateMainContent(self.page)
        
        # Create main row layout
        main_row = ft.Row([
            sidebar,
            main_content
        ], expand=True, spacing=0)
        
        self.page.add(main_row)
    
    def OnSpeedAnalysisClick(self, e):
        """
        Handle speed analysis button click.
        
        Args:
            e: Event object
        """
        self.main_content_component.ShowSpeedAnalysis()
        self.page.update()
    
    def OnSeoAnalysisClick(self, e):
        """
        Handle SEO analysis button click.
        
        Args:
            e: Event object
        """
        self.main_content_component.ShowSeoAnalysis()
        self.page.update()
    
    def OnBugAnalysisClick(self, e):
        """
        Handle bug analysis button click.
        
        Args:
            e: Event object
        """
        self.main_content_component.ShowBugAnalysis()
        self.page.update()

def main(page: ft.Page):
    """
    Main entry point for the application.
    
    Args:
        page (ft.Page): The Flet page object
    """
    app = NinjaAnalyzerApp()
    app.SetupPage(page)

if __name__ == "__main__":
    ft.app(target=main)