"""
Sidebar component for the Ninja Analyzer application.
This module contains the sidebar component with navigation buttons.
"""

import flet as ft

class SidebarComponent:
    """
    Sidebar component class that handles the sidebar UI and functionality.
    """
    
    def __init__(self, on_speed_click, on_seo_click, on_bug_click):
        """
        Initialize the sidebar component.
        
        Args:
            on_speed_click (callable): Callback function for speed analysis button
            on_seo_click (callable): Callback function for SEO analysis button
            on_bug_click (callable): Callback function for bug analysis button
        """
        self.on_speed_click = on_speed_click
        self.on_seo_click = on_seo_click
        self.on_bug_click = on_bug_click
        self.container = None
        
    def CreateSidebar(self):
        """
        Creates and returns the sidebar container.
        
        Returns:
            ft.Container: The sidebar container
        """
        self.container = ft.Container(
            content=ft.Column([
                # Title section
                ft.Text(
                    "Ninja Analyzer", 
                    size=20, 
                    weight=ft.FontWeight.BOLD, 
                    color=ft.Colors.WHITE, 
                    font_family="Iransans-Bold"
                ),
                ft.Divider(color=ft.Colors.WHITE, height=20),
                
                # Navigation buttons
                ft.ElevatedButton(
                    "Speed Analysis",
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.CYAN,
                    width=210,
                    height=40,
                    icon=ft.Icons.SPEED,
                    on_click=self.on_speed_click
                ),
                ft.ElevatedButton(
                    "SEO Analysis",
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.CYAN,
                    width=210,
                    height=40,
                    icon=ft.Icons.SEARCH,
                    on_click=self.on_seo_click
                ),
                ft.ElevatedButton(
                    "Bug Detection",
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.CYAN,
                    width=210,
                    height=40,
                    icon=ft.Icons.BUG_REPORT,
                    on_click=self.on_bug_click
                ),
            ], scroll=ft.ScrollMode.AUTO, spacing=10),
            bgcolor=ft.Colors.CYAN,
            width=250,
            height=800,
            padding=20,
            border_radius=ft.border_radius.all(8)
        )
        
        return self.container
