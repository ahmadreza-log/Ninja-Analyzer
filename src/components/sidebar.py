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
                # Header with gradient background
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "⚡ Ninja Analyzer", 
                            size=24, 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.WHITE, 
                            font_family="Iransans-Bold"
                        ),
                        ft.Text(
                            "Website Performance Tool",
                            size=12,
                            color=ft.Colors.WHITE70,
                            font_family="Iransans-Regular"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.CYAN_700,
                    padding=20,
                    border_radius=ft.border_radius.only(top_left=8, top_right=8)
                ),
                
                # Navigation section
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Analysis Tools",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.CYAN_800,
                            font_family="Iransans-Bold"
                        ),
                        ft.Divider(color=ft.Colors.CYAN_200, height=10),
                        
                        # Navigation buttons with improved styling
                        ft.Container(
                            content=ft.ElevatedButton(
                                "🚀 Speed Analysis",
                                bgcolor=ft.Colors.WHITE,
                                color=ft.Colors.CYAN_700,
                                width=220,
                                height=50,
                                icon=ft.Icons.SPEED,
                                on_click=self.on_speed_click,
                                style=ft.ButtonStyle(
                                    elevation=2,
                                    shadow_color=ft.Colors.CYAN_200
                                )
                            ),
                            margin=ft.margin.only(bottom=10)
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(
                                "🔍 SEO Analysis",
                                bgcolor=ft.Colors.WHITE,
                                color=ft.Colors.CYAN_700,
                                width=220,
                                height=50,
                                icon=ft.Icons.SEARCH,
                                on_click=self.on_seo_click,
                                style=ft.ButtonStyle(
                                    elevation=2,
                                    shadow_color=ft.Colors.CYAN_200
                                )
                            ),
                            margin=ft.margin.only(bottom=10)
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(
                                "🐛 Bug Detection",
                                bgcolor=ft.Colors.WHITE,
                                color=ft.Colors.CYAN_700,
                                width=220,
                                height=50,
                                icon=ft.Icons.BUG_REPORT,
                                on_click=self.on_bug_click,
                                style=ft.ButtonStyle(
                                    elevation=2,
                                    shadow_color=ft.Colors.CYAN_200
                                )
                            ),
                            margin=ft.margin.only(bottom=10)
                        ),
                    ], scroll=ft.ScrollMode.AUTO, spacing=5),
                    padding=20,
                    expand=True
                )
            ], spacing=0),
            bgcolor=ft.Colors.CYAN_100,
            width=280,
            height=900,
            border_radius=ft.border_radius.all(0),
            border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.CYAN_200)),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.CYAN_100,
                offset=ft.Offset(2, 0)
            )
        )
        
        return self.container
