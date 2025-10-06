"""
Speed Analysis Page for Ninja Analyzer.
This module handles website speed analysis functionality similar to PageSpeed Insights.
"""

import flet as ft
import time
from src.pages.base_page import BasePage
from src.services.http_client import HttpClient
from src.utils.url import extract_host, normalize_url
from src.utils.bytes import format_bytes

class SpeedAnalysisPage(BasePage):
    """
    Speed analysis page class that handles website speed testing.
    """
    
    def __init__(self):
        """Initialize the speed analysis page."""
        self.url_input = None
        self.analyze_button = None
        self.results_container = None
        self.loading_indicator = None
        self.advanced_options = None
        self.toggle_advanced = None
        super().__init__()
        self.http = HttpClient()
        
        # Advanced options state
        self.multiple_test = False
        self.deep_test = True
        self.browser_test = True
        self.mobile_test = False
        self.test_count = 3
        
    def CreateSpeedAnalysisPage(self):
        """
        Creates and returns the speed analysis page content.
        
        Returns:
            ft.Column: The speed analysis page content
        """
        # URL input field with improved styling
        self.url_input = ft.TextField(
            label="🌐 Website URL",
            hint_text="Enter website URL (e.g., https://google.com)",
            expand=True,
            border_color=ft.Colors.CYAN_300,
            focused_border_color=ft.Colors.CYAN_600,
            border_radius=ft.border_radius.all(10),
            content_padding=ft.padding.all(15),
            text_size=16,
            prefix_icon=ft.Icons.LINK,
            style=ft.TextFieldStyle(
                border_color=ft.Colors.CYAN_300,
                focused_border_color=ft.Colors.CYAN_600,
                border_width=2
            )
        )
        
        # Analyze button with improved styling
        self.analyze_button = ft.ElevatedButton(
            "🚀 Start Analysis",
            bgcolor=ft.Colors.CYAN_600,
            color=ft.Colors.WHITE,
            width=220,
            height=55,
            icon=ft.Icons.SPEED,
            on_click=self.OnAnalyzeClick,
            style=ft.ButtonStyle(
                elevation=3,
                shadow_color=ft.Colors.CYAN_300,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        
        # Advanced options with modern design
        self.advanced_options = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.CYAN_600, size=20),
                        ft.Text("⚙️ Advanced Options", size=18, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold", color=ft.Colors.CYAN_800)
                    ]),
                    padding=ft.padding.only(bottom=15)
                ),
                
                # Options grid
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Checkbox(
                                    label="🔄 Multiple Tests",
                                    value=False,
                                    on_change=self.OnMultipleTestChange,
                                    active_color=ft.Colors.CYAN_600
                                ),
                                padding=10,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=ft.border_radius.all(8),
                                border=ft.border.all(1, ft.Colors.CYAN_200)
                            ),
                            ft.Container(
                                content=ft.Checkbox(
                                    label="🔍 Deep Analysis",
                                    value=False,
                                    on_change=self.OnDeepTestChange,
                                    active_color=ft.Colors.CYAN_600
                                ),
                                padding=10,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=ft.border_radius.all(8),
                                border=ft.border.all(1, ft.Colors.CYAN_200)
                            ),
                            ft.Container(
                                content=ft.Checkbox(
                                    label="📱 Mobile Test",
                                    value=False,
                                    on_change=self.OnMobileTestChange,
                                    active_color=ft.Colors.CYAN_600
                                ),
                                padding=10,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=ft.border_radius.all(8),
                                border=ft.border.all(1, ft.Colors.CYAN_200)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        
                        ft.Divider(height=20),
                        
                        # Test count slider
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.REPEAT, color=ft.Colors.CYAN_600, size=16),
                                    ft.Text("Test Count:", size=14, font_family="Iransans-Bold", color=ft.Colors.CYAN_800)
                                ]),
                                ft.Slider(
                                    min=1,
                                    max=10,
                                    divisions=9,
                                    value=3,
                                    label="Test {value}",
                                    on_change=self.OnTestCountChange,
                                    active_color=ft.Colors.CYAN_600,
                                    inactive_color=ft.Colors.CYAN_200
                                )
                            ]),
                            padding=15,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=ft.border_radius.all(8),
                            border=ft.border.all(1, ft.Colors.CYAN_200)
                        ),
                        
                        ft.Divider(height=15),
                        
                        # Browser test option
                        ft.Container(
                            content=ft.Row([
                                ft.Checkbox(
                                    label="🌐 Real Browser Load (Headless)",
                                    value=True,
                                    on_change=self.OnBrowserTestChange,
                                    active_color=ft.Colors.CYAN_600
                                ),
                                ft.Text("(requires playwright)", size=12, color=ft.Colors.GREY_600)
                            ]),
                            padding=15,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=ft.border_radius.all(8),
                            border=ft.border.all(1, ft.Colors.CYAN_200)
                        )
                    ], spacing=10),
                    padding=20
                )
            ]),
            bgcolor=ft.Colors.CYAN_50,
            border_radius=ft.border_radius.all(12),
            border=ft.border.all(2, ft.Colors.CYAN_200),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.CYAN_100,
                offset=ft.Offset(0, 2)
            ),
            padding=20,
            visible=False
        )
        
        # Toggle advanced options button
        self.toggle_advanced = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            tooltip="Advanced Options",
            on_click=self.OnToggleAdvanced
        )
        
        # Loading indicator with animation
        self.loading_indicator = ft.Container(
            content=ft.Column([
                ft.ProgressRing(
                    visible=False,
                    width=40,
                    height=40,
                    stroke_width=4,
                    color=ft.Colors.CYAN_600
                ),
                ft.Text(
                    "Analyzing...",
                    size=12,
                    color=ft.Colors.CYAN_600,
                    font_family="Iransans-Regular"
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            visible=False
        )
        
        # Results container with modern design
        self.results_container = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.CYAN_600, size=24),
                            ft.Text(
                                "📊 Analysis Results",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.CYAN_800,
                                font_family="Iransans-Bold"
                            )
                        ]),
                        ft.Text(
                            "Speed analysis results will be displayed here. Enter a URL and click 'Start Analysis' to begin.",
                            size=14,
                            color=ft.Colors.GREY_600,
                            font_family="Iransans-Regular"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=30,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.border_radius.all(15),
                    border=ft.border.all(2, ft.Colors.CYAN_200),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.Colors.CYAN_100,
                        offset=ft.Offset(0, 2)
                    )
                )
            ], scroll=ft.ScrollMode.AUTO, spacing=15),
            padding=20,
            bgcolor=ft.Colors.GREY_50,
            border_radius=ft.border_radius.all(15),
            expand=True
        )
        
        # Main page content with improved layout
        page_content = ft.Column([
            # Header with gradient background
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.SPEED, color=ft.Colors.WHITE, size=32),
                        ft.Text(
                            "🚀 Website Speed Analysis",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            font_family="Iransans-Bold",
                            color=ft.Colors.WHITE
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(
                        "Analyze your website's performance and get detailed insights",
                        size=16,
                        color=ft.Colors.WHITE_70,
                        font_family="Iransans-Regular"
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                bgcolor=ft.Colors.CYAN_600,
                padding=30,
                border_radius=ft.border_radius.all(15),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.CYAN_300,
                    offset=ft.Offset(0, 4)
                )
            ),
            
            # Input section with card design
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🌐 Enter the website URL to analyze:",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        font_family="Iransans-Bold",
                        color=ft.Colors.CYAN_800
                    ),
                    ft.Row([
                        self.url_input,
                        self.analyze_button,
                        self.toggle_advanced,
                        self.loading_indicator
                    ], alignment=ft.MainAxisAlignment.START, spacing=20),
                ], spacing=20),
                bgcolor=ft.Colors.WHITE,
                padding=25,
                border_radius=ft.border_radius.all(12),
                border=ft.border.all(1, ft.Colors.CYAN_200),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.Colors.CYAN_100,
                    offset=ft.Offset(0, 2)
                )
            ),
            
            # Advanced options
            self.advanced_options,
            
            # Results section
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📈 Analysis Results",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        font_family="Iransans-Bold",
                        color=ft.Colors.CYAN_800
                    ),
                    self.results_container
                ], spacing=15),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=ft.border_radius.all(12),
                border=ft.border.all(1, ft.Colors.CYAN_200),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.Colors.CYAN_100,
                    offset=ft.Offset(0, 2)
                ),
                expand=True
            )
            
        ], scroll=ft.ScrollMode.AUTO, spacing=25)
        
        return page_content
    
    def OnAnalyzeClick(self, e):
        """
        Handle analyze button click event.
        
        Args:
            e: Event object
        """
        url = normalize_url(self.url_input.value.strip())
        if not url:
            self.ShowErrorMessage("Please enter a URL.")
            return
            
        # Show loading
        self.ShowLoading()
        
        # Perform analysis
        self.PerformSpeedAnalysis(url)
    
    def ShowLoading(self):
        """Show loading indicator and disable button."""
        self.loading_indicator.visible = True
        self.analyze_button.disabled = True
        self.analyze_button.text = "Analyzing..."
        self.page.update()
    
    def HideLoading(self):
        """Hide loading indicator and enable button."""
        self.loading_indicator.visible = False
        self.analyze_button.disabled = False
        self.analyze_button.text = "Start Speed Analysis"
        self.page.update()
    
    def ShowErrorMessage(self, message):
        """
        Show error message in results container.
        
        Args:
            message (str): Error message to display
        """
        self.results_container.content.controls.clear()
        self.results_container.content.controls.append(
            ft.Text(
                f"❌ {message}",
                size=16,
                color=ft.Colors.RED,
                font_family="Iransans-Regular"
            )
        )
        self.page.update()
    
    def PerformSpeedAnalysis(self, url):
        """
        Perform speed analysis on the given URL with advanced options.
        
        Args:
            url (str): URL to analyze
        """
        try:
            all_results = []
            
            # Perform multiple tests if enabled
            test_count = self.test_count if self.multiple_test else 1
            
            for i in range(test_count):
                # Pre-request network measurements (DNS lookup)
                dns_lookup_ms = None
                try:
                    host = extract_host(url)
                    import socket
                    _t0 = time.time()
                    socket.getaddrinfo(host, None)
                    _t1 = time.time()
                    dns_lookup_ms = round((_t1 - _t0) * 1000, 2)
                except Exception:
                    dns_lookup_ms = None
                # Add mobile user agent if mobile test is enabled
                headers = {}
                if self.mobile_test:
                    headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
                # Encourage compression support (including br)
                headers['Accept-Encoding'] = 'br, gzip, deflate'
                
                # Measure response via HttpClient
                http_resp = self.http.get(url, headers=headers, allow_redirects=True)
                response = http_resp.response
                response_time = http_resp.elapsed_ms
                # requests exposes time to first byte via elapsed
                ttfb_ms = round(response.elapsed.total_seconds() * 1000, 2) if getattr(response, 'elapsed', None) else None
                content_length = len(response.content)
                status_code = response.status_code
                
                # Full page load: prefer real browser if enabled, else simulate
                if self.browser_test:
                    full_load_time = self.CollectRealBrowserMetrics(url, self.mobile_test)
                else:
                    full_load_time = self.SimulateFullPageLoad(response.text, response_time)
                
                # Calculate DOM Content Loaded time
                dom_ready_time = self.CalculateDOMReadyTime(response_time, content_length)
                
                # Get response headers
                response_headers = response.headers
                content_type = response_headers.get('content-type', 'Unknown')
                server = response_headers.get('server', 'Unknown')
                content_encoding = response_headers.get('content-encoding', 'none')
                cache_control = response_headers.get('cache-control', 'None')
                expires_hdr = response_headers.get('expires', 'None')
                # HTTP version (requests uses urllib3 raw.version: 11 => HTTP/1.1)
                try:
                    raw_ver = getattr(response.raw, 'version', None)
                    http_version = 'HTTP/1.1' if raw_ver == 11 else 'HTTP/1.0' if raw_ver == 10 else 'HTTP/2 (proxy)' if raw_ver == 20 else 'Unknown'
                except Exception:
                    http_version = 'Unknown'
                redirect_count = len(getattr(response, 'history', []) or [])
                # Best-practice analysis on HTML when applicable
                best_practices = {}
                try:
                    if 'text/html' in content_type.lower():
                        best_practices = self.AnalyzeHtmlBestPractices(response.text)
                except Exception:
                    best_practices = {}
                # CDN heuristic
                cdn = self.DetectCdn(server, response_headers)
                
                # Deep analysis if enabled
                if self.deep_test:
                    # Analyze additional metrics
                    expires = expires_hdr
                    last_modified = response_headers.get('last-modified', 'None')
                    etag = response_headers.get('etag', 'None')
                    connection = response_headers.get('connection', 'None')
                    keep_alive = response_headers.get('keep-alive', 'None')
                    
                    # Calculate additional performance metrics
                    # Prefer real TTFB if available
                    ttf = ttfb_ms if ttfb_ms is not None else self.CalculateTimeToFirstByte(response_time)
                    lcp = self.CalculateLargestContentfulPaint(content_length)
                    cls = self.CalculateCumulativeLayoutShift(content_length)
                    fid = self.CalculateFirstInputDelay(response_time)
                    
                    # Analyze content structure
                    content_analysis = self.AnalyzeContentStructure(response.text)
                    
                    # Security headers analysis
                    security_headers = self.AnalyzeSecurityHeaders(response_headers)
                    
                    # Performance grade calculation
                    performance_grade = self.CalculatePerformanceGrade(response_time, content_length, response_headers)
                    
                    result = {
                        'url': url,
                        'response_time': response_time,
                        'content_size': content_length,
                        'status_code': status_code,
                        'content_type': content_type,
                        'server': server,
                        'http_version': http_version,
                        'redirects': redirect_count,
                        'compression': content_encoding,
                        'cache_control': cache_control,
                        'expires': expires,
                        'last_modified': last_modified,
                        'etag': etag,
                        'connection': connection,
                        'keep_alive': keep_alive,
                        'ttf': ttf,
                        'lcp': lcp,
                        'cls': cls,
                        'fid': fid,
                        'dns': dns_lookup_ms,
                        'cdn': cdn,
                        'best_practices': best_practices,
                        'full_load_time': full_load_time,
                        'dom_ready_time': dom_ready_time,
                        'content_analysis': content_analysis,
                        'security_headers': security_headers,
                        'performance_grade': performance_grade,
                        'test_number': i + 1,
                        'mobile_test': self.mobile_test
                    }
                else:
                    result = {
                        'url': url,
                        'response_time': response_time,
                        'content_size': content_length,
                        'status_code': status_code,
                        'content_type': content_type,
                        'server': server,
                        'http_version': http_version,
                        'redirects': redirect_count,
                        'compression': content_encoding,
                        'dns': dns_lookup_ms,
                        'cdn': cdn,
                        'best_practices': best_practices,
                        'full_load_time': full_load_time,
                        'dom_ready_time': dom_ready_time,
                        'test_number': i + 1,
                        'mobile_test': self.mobile_test
                    }
                
                all_results.append(result)
            
            # Display results
            if self.multiple_test:
                self.DisplayMultipleTestResults(all_results)
            else:
                self.DisplaySpeedResults(all_results[0])
            
        except Exception as ex:
            msg = str(ex)
            if 'timeout' in msg.lower():
                self.ShowErrorMessage("Connection timeout. Please try again.")
            elif 'failed to establish a new connection' in msg.lower() or 'connection' in msg.lower():
                self.ShowErrorMessage("Connection error. Please check the URL.")
            else:
                self.ShowErrorMessage(f"Analysis error: {str(ex)}")
        finally:
            self.HideLoading()
    
    def CalculateTimeToFirstByte(self, response_time):
        """Calculate Time to First Byte (TTFB)."""
        return response_time * 0.3  # Simulate TTFB calculation
    
    def CalculateLargestContentfulPaint(self, content_size):
        """Calculate Largest Contentful Paint (LCP)."""
        # Simulate LCP based on content size
        if content_size < 1024 * 1024:  # < 1MB
            return 1.2
        elif content_size < 5 * 1024 * 1024:  # < 5MB
            return 2.5
        else:
            return 4.0
    
    def CalculateCumulativeLayoutShift(self, content_size):
        """Calculate Cumulative Layout Shift (CLS)."""
        # Simulate CLS based on content size
        if content_size < 500 * 1024:  # < 500KB
            return 0.05
        elif content_size < 1024 * 1024:  # < 1MB
            return 0.15
        else:
            return 0.25
    
    def CalculateFirstInputDelay(self, response_time):
        """Calculate First Input Delay (FID)."""
        # Simulate FID based on response time
        if response_time < 200:
            return 50
        elif response_time < 500:
            return 100
        else:
            return 200
    
    def AnalyzeContentStructure(self, html_content):
        """Analyze HTML content structure."""
        import re
        
        # Count various elements
        img_count = len(re.findall(r'<img[^>]*>', html_content, re.IGNORECASE))
        link_count = len(re.findall(r'<a[^>]*href=', html_content, re.IGNORECASE))
        script_count = len(re.findall(r'<script[^>]*>', html_content, re.IGNORECASE))
        style_count = len(re.findall(r'<style[^>]*>', html_content, re.IGNORECASE))
        div_count = len(re.findall(r'<div[^>]*>', html_content, re.IGNORECASE))
        
        # Check for performance issues
        inline_styles = len(re.findall(r'style\s*=', html_content, re.IGNORECASE))
        external_scripts = len(re.findall(r'<script[^>]*src=', html_content, re.IGNORECASE))
        external_styles = len(re.findall(r'<link[^>]*rel\s*=\s*["\']stylesheet["\']', html_content, re.IGNORECASE))
        
        return {
            'img_count': img_count,
            'link_count': link_count,
            'script_count': script_count,
            'style_count': style_count,
            'div_count': div_count,
            'inline_styles': inline_styles,
            'external_scripts': external_scripts,
            'external_styles': external_styles
        }
    
    def AnalyzeSecurityHeaders(self, headers):
        """Analyze security headers."""
        security_headers = {
            'https': headers.get('strict-transport-security', 'None'),
            'x_frame_options': headers.get('x-frame-options', 'None'),
            'x_content_type': headers.get('x-content-type-options', 'None'),
            'x_xss_protection': headers.get('x-xss-protection', 'None'),
            'content_security_policy': headers.get('content-security-policy', 'None'),
            'referrer_policy': headers.get('referrer-policy', 'None')
        }
        
        # Calculate security score
        security_score = 0
        for header, value in security_headers.items():
            if value != 'None':
                security_score += 1
        
        security_headers['score'] = security_score
        security_headers['grade'] = 'Excellent' if security_score >= 5 else 'Good' if security_score >= 3 else 'Average' if security_score >= 1 else 'Poor'
        
        return security_headers

    def AnalyzeHtmlBestPractices(self, html_content):
        """Analyze HTML against common best practices.
        Returns a dict of booleans and counts to be surfaced in the UI.
        """
        import re
        out = {}
        # meta viewport for mobile friendliness
        out['has_viewport'] = bool(re.search(r'<meta[^>]+name=["\']viewport["\']', html_content, re.IGNORECASE))
        # title tag
        out['has_title'] = bool(re.search(r'<title>.*?</title>', html_content, re.IGNORECASE|re.DOTALL))
        # description meta
        out['has_meta_description'] = bool(re.search(r'<meta[^>]+name=["\']description["\']', html_content, re.IGNORECASE))
        # lazy loading images
        out['lazy_loaded_images'] = len(re.findall(r'<img[^>]*loading=["\']lazy["\']', html_content, re.IGNORECASE))
        # critical CSS hint
        out['has_preload_css'] = bool(re.search(r'<link[^>]+rel=["\']preload["\'][^>]+as=["\']style["\']', html_content, re.IGNORECASE))
        # http resources (mixed content risk)
        out['http_resources'] = len(re.findall(r'\shref=\"http://|\ssrc=\"http://', html_content, re.IGNORECASE))
        return out

    def DetectCdn(self, server, headers):
        """Heuristic CDN detection based on server/header signatures."""
        sigs = ['cloudflare', 'akamai', 'fastly', 'cloudfront', 'cdn77', 'incapsula', 'cachefly']
        blob = (server or '') + ' ' + ' '.join([f"{k}:{v}" for k, v in headers.items()])
        blob = blob.lower()
        for s in sigs:
            if s in blob:
                return s
        return 'unknown'
    
    def SimulateFullPageLoad(self, html_content, base_response_time):
        """
        Simulate full page load time including all resources.
        This is a realistic simulation based on HTML content analysis.
        """
        import re
        
        # Count external resources
        css_files = len(re.findall(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']stylesheet["\']', html_content, re.IGNORECASE))
        js_files = len(re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE))
        images = len(re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE))
        
        # Calculate additional load time based on resources
        additional_time = 0
        
        # CSS files (typically fast)
        additional_time += css_files * 50  # 50ms per CSS file
        
        # JavaScript files (can be slow)
        additional_time += js_files * 100  # 100ms per JS file
        
        # Images (can be very slow)
        additional_time += images * 200  # 200ms per image
        
        # Network latency simulation
        network_delay = 50  # Base network delay
        
        # Calculate total load time
        total_load_time = base_response_time + additional_time + network_delay
        
        return {
            'total_load_time': round(total_load_time, 2),
            'css_files': css_files,
            'js_files': js_files,
            'images': images,
            'additional_time': round(additional_time, 2)
        }

    def CollectRealBrowserMetrics(self, url, is_mobile=False):
        """Collect real page load metrics using a headless browser (playwright).
        Returns a dict compatible with SimulateFullPageLoad output keys.
        If playwright is not installed, falls back to simulation with a flag.
        """
        try:
            from playwright.sync_api import sync_playwright
        except Exception:
            # Fallback marker
            return {
                'total_load_time': 0,
                'css_files': 0,
                'js_files': 0,
                'images': 0,
                'additional_time': 0,
                'fallback': 'playwright_not_installed'
            }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={ 'width': 390, 'height': 844 } if is_mobile else { 'width': 1366, 'height': 768 },
                user_agent=(
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
                    if is_mobile
                    else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
            )
            page = context.new_page()
            # Track network requests
            resources = { 'css': 0, 'js': 0, 'img': 0 }
            def on_request(req):
                url = req.url.lower()
                if url.endswith('.css'):
                    resources['css'] += 1
                elif url.endswith('.js'):
                    resources['js'] += 1
                elif any(url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']):
                    resources['img'] += 1
            page.on('request', on_request)

            import time as _t
            t0 = _t.time()
            page.goto(url, wait_until='load', timeout=30000)
            # Ensure network idle-ish
            try:
                page.wait_for_load_state('networkidle', timeout=5000)
            except Exception:
                pass
            t1 = _t.time()
            browser.close()

            total_ms = round((t1 - t0) * 1000, 2)
            # Approximate additional time (beyond initial response unknown here)
            additional = max(0, total_ms - 0)
            return {
                'total_load_time': total_ms,
                'css_files': resources['css'],
                'js_files': resources['js'],
                'images': resources['img'],
                'additional_time': additional,
                'fallback': None
            }
    
    def CalculateDOMReadyTime(self, response_time, content_size):
        """
        Calculate DOM Content Loaded time.
        This is when the HTML document has been completely loaded and parsed.
        """
        # DOM ready is typically 70-80% of total response time
        dom_ready_ratio = 0.75
        
        # Adjust based on content size (larger content = longer parsing)
        if content_size > 1024 * 1024:  # > 1MB
            dom_ready_ratio = 0.85
        elif content_size > 500 * 1024:  # > 500KB
            dom_ready_ratio = 0.80
        else:
            dom_ready_ratio = 0.70
            
        return round(response_time * dom_ready_ratio, 2)
    
    def CalculatePerformanceGrade(self, response_time, content_size, headers):
        """Calculate overall performance grade."""
        score = 100
        
        # Response time penalty
        if response_time > 3000:
            score -= 30
        elif response_time > 2000:
            score -= 20
        elif response_time > 1000:
            score -= 10
        
        # Content size penalty
        if content_size > 10 * 1024 * 1024:  # > 10MB
            score -= 25
        elif content_size > 5 * 1024 * 1024:  # > 5MB
            score -= 15
        elif content_size > 2 * 1024 * 1024:  # > 2MB
            score -= 10
        
        # Cache headers bonus
        if headers.get('cache-control'):
            score += 5
        if headers.get('expires'):
            score += 5
        
        # Compression bonus
        if headers.get('content-encoding'):
            score += 10
        
        # Security headers bonus
        security_headers = ['strict-transport-security', 'x-frame-options', 'x-content-type-options']
        for header in security_headers:
            if headers.get(header):
                score += 2
        
        return {
            'score': max(0, min(100, score)),
            'grade': 'A+' if score >= 95 else 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F'
        }
    
    def DisplayMultipleTestResults(self, results):
        """Display results for multiple tests."""
        self.results_container.content.controls.clear()
        
        # Header
        self.results_container.content.controls.append(
            ft.Text(
                f"Results of {len(results)} tests: {results[0]['url']}",
                size=24,
                weight=ft.FontWeight.BOLD,
                font_family="Iransans-Bold",
                color=ft.Colors.CYAN_700
            )
        )
        
        # Calculate averages
        avg_response_time = sum(r['response_time'] for r in results) / len(results)
        avg_content_size = sum(r['content_size'] for r in results) / len(results)
        
        # Summary card
        summary_card = ft.Container(
            content=ft.Column([
                ft.Text("Results Summary", size=18, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                ft.Text(f"Average Response Time: {avg_response_time:.2f} ms", size=14, font_family="Iransans-Regular"),
                ft.Text(f"Average Size: {format_bytes(avg_content_size)}", size=14, font_family="Iransans-Regular"),
                ft.Text(f"Test Count: {len(results)}", size=14, font_family="Iransans-Regular"),
            ]),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            padding=15,
            border=ft.border.all(1, ft.Colors.CYAN_200)
        )
        
        self.results_container.content.controls.append(summary_card)
        
        # Individual test results
        for i, result in enumerate(results):
            test_card = ft.Container(
                content=ft.Column([
                    ft.Text(f"Test {i + 1}", size=16, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                    ft.Text(f"Response Time: {result['response_time']} ms", size=12, font_family="Iransans-Regular"),
                    ft.Text(f"Size: {format_bytes(result['content_size'])}", size=12, font_family="Iransans-Regular"),
                    ft.Text(f"Status Code: {result['status_code']}", size=12, font_family="Iransans-Regular"),
                ]),
                bgcolor=ft.Colors.GREY_50,
                border_radius=ft.border_radius.all(8),
                padding=10,
                width=200
            )
            
            self.results_container.content.controls.append(test_card)
        
        self.page.update()
    
    def DisplaySpeedResults(self, results):
        """
        Display comprehensive speed analysis results with charts.
        
        Args:
            results (dict): Analysis results dictionary
        """
        self.results_container.content.controls.clear()
        
        # Header with URL and timestamp
        header_info = ft.Container(
            content=ft.Column([
                ft.Text(
                    f"Complete Analysis Report: {results['url']}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    font_family="Iransans-Bold",
                    color=ft.Colors.CYAN_700
                ),
                ft.Text(
                    f"Date and Time: {self.current_datetime()}",
                    size=14,
                    color=ft.Colors.GREY_600,
                    font_family="Iransans-Regular"
                ),
                ft.Text(
                    f"Test Type: {'Mobile' if results.get('mobile_test', False) else 'Desktop'}",
                    size=14,
                    color=ft.Colors.GREY_600,
                    font_family="Iransans-Regular"
                )
            ]),
            bgcolor=ft.Colors.CYAN_50,
            border_radius=ft.border_radius.all(10),
            padding=15,
            border=ft.border.all(1, ft.Colors.CYAN_200)
        )
        
        self.results_container.content.controls.append(header_info)
        
        # Performance Score with Circle Chart
        performance_score = self.CalculatePerformanceScore(results['response_time'])
        score_color = self.GetPerformanceColor(performance_score)
        
        # Create performance score card
        score_card = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Performance Score",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    font_family="Iransans-Bold"
                ),
                ft.Text(
                    f"{performance_score}/100",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=score_color,
                    font_family="Iransans-Bold"
                ),
                ft.Text(
                    self.GetPerformanceLabel(performance_score),
                    size=14,
                    color=score_color,
                    font_family="Iransans-Regular"
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            padding=20,
            border=ft.border.all(2, score_color),
            width=200
        )
        
        # Create comprehensive metrics cards (row 1)
        metrics_row = ft.Row([
            self.CreateMetricCard("Response", f"{results['response_time']} ms", ft.Icons.SPEED),
            self.CreateMetricCard("Full Load", f"{results.get('full_load_time', {}).get('total_load_time', 0)} ms", ft.Icons.DOWNLOAD),
            self.CreateMetricCard("DOM Ready", f"{results.get('dom_ready_time', 0)} ms", ft.Icons.PLAY_ARROW),
            self.CreateMetricCard("Size", format_bytes(results['content_size']), ft.Icons.STORAGE),
            self.CreateMetricCard("Status", str(results['status_code']), ft.Icons.CHECK_CIRCLE),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True)
        
        # Additional metrics row (row 2)
        additional_metrics_row = ft.Row([
            self.CreateMetricCard("Type", results['content_type'].split(';')[0][:20] + "...", ft.Icons.CODE),
            self.CreateMetricCard("Server", results['server'][:18] + ("..." if len(results['server'])>18 else ""), ft.Icons.DNS),
            self.CreateMetricCard("HTTP", results.get('http_version', 'unknown'), ft.Icons.HTTP),
            self.CreateMetricCard("Redirects", str(results.get('redirects', 0)), ft.Icons.REDO),
            self.CreateMetricCard("Compress", results.get('compression', 'none'), ft.Icons.COMPRESS),
            self.CreateMetricCard("DNS", (str(results.get('dns')) + " ms") if results.get('dns') else "-", ft.Icons.TRAVEL_EXPLORE),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True)

        # Resources analysis
        resources = results.get('full_load_time', {}) or {}
        resources_row = ft.Row([
            self.CreateMetricCard("CSS Files", str(resources.get('css_files', 0)), ft.Icons.STYLE),
            self.CreateMetricCard("JS Files", str(resources.get('js_files', 0)), ft.Icons.CODE),
            self.CreateMetricCard("Images", str(resources.get('images', 0)), ft.Icons.IMAGE),
            self.CreateMetricCard("Extra Time", f"{resources.get('additional_time', 0)} ms", ft.Icons.TIMER),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True)
        
        # Best practices quick badges
        best = results.get('best_practices', {}) or {}
        best_row = ft.Row([
            self.CreateMetricCard("Viewport", "OK" if best.get('has_viewport') else "Missing", ft.Icons.PHONE_ANDROID),
            self.CreateMetricCard("Title", "OK" if best.get('has_title') else "Missing", ft.Icons.TITLE),
            self.CreateMetricCard("Meta Desc", "OK" if best.get('has_meta_description') else "Missing", ft.Icons.DESCRIPTION),
            self.CreateMetricCard("Lazy Img", str(best.get('lazy_loaded_images', 0)), ft.Icons.IMAGE),
            self.CreateMetricCard("Preload CSS", "Yes" if best.get('has_preload_css') else "No", ft.Icons.DOWNLOAD),
            self.CreateMetricCard("HTTP res", str(best.get('http_resources', 0)), ft.Icons.SIGNAL_WIFI_OFF),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True)
        
        # Additional performance metrics if deep test is enabled
        if 'ttf' in results and 'lcp' in results:
            advanced_metrics = ft.Row([
                self.CreateMetricCard("TTFB", f"{results['ttf']:.1f} ms", ft.Icons.TIMER),
                self.CreateMetricCard("LCP", f"{results['lcp']:.1f} s", ft.Icons.VISIBILITY),
                self.CreateMetricCard("CLS", f"{results.get('cls', 0):.2f}", ft.Icons.SWAP_HORIZ),
                self.CreateMetricCard("FID", f"{results.get('fid', 0)} ms", ft.Icons.TOUCH_APP),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True)
            
            # Performance grade card
            if 'performance_grade' in results:
                grade_card = ft.Container(
                    content=ft.Column([
                        ft.Text("Overall Grade", size=16, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                        ft.Text(f"{results['performance_grade']['grade']}", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN, font_family="Iransans-Bold"),
                        ft.Text(f"{results['performance_grade']['score']}/100", size=14, color=ft.Colors.GREY_600, font_family="Iransans-Regular")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.border_radius.all(10),
                    padding=15,
                    border=ft.border.all(2, ft.Colors.GREEN),
                    width=150
                )
            else:
                grade_card = None
        else:
            advanced_metrics = None
            grade_card = None
        
        # Create pie chart for performance breakdown
        pie_chart = self.CreatePerformancePieChart(results)
        
        # Detailed metrics section
        detailed_metrics = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Technical Details",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    font_family="Iransans-Bold"
                ),
                ft.Divider(),
                self.CreateDetailRow("Content Type", results['content_type']),
                self.CreateDetailRow("Server", results['server']),
                self.CreateDetailRow("Analysis Date", self.current_datetime()),
                self.CreateDetailRow("Total Analysis Time", f"{results['response_time']} milliseconds"),
                self.CreateDetailRow("Page Size", format_bytes(results['content_size'])),
                self.CreateDetailRow("HTTP Status Code", str(results['status_code'])),
                self.CreateDetailRow("Test Type", 'Mobile' if results.get('mobile_test', False) else 'Desktop'),
            ]),
            bgcolor=ft.Colors.GREY_50,
            border_radius=ft.border_radius.all(10),
            padding=15
        )
        
        # Additional technical details if deep test is enabled
        if 'cache_control' in results:
            cache_details = ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Cache and Optimization Details",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        font_family="Iransans-Bold"
                    ),
                    ft.Divider(),
                    self.CreateDetailRow("Cache Control", results.get('cache_control', 'None')),
                    self.CreateDetailRow("Expires", results.get('expires', 'None')),
                    self.CreateDetailRow("Last Modified", results.get('last_modified', 'None')),
                    self.CreateDetailRow("TTFB", f"{results.get('ttf', 0):.1f} ms"),
                    self.CreateDetailRow("LCP", f"{results.get('lcp', 0):.1f} s"),
                ]),
                bgcolor=ft.Colors.BLUE_50,
                border_radius=ft.border_radius.all(10),
                padding=15
            )
        else:
            cache_details = None
        
        # Performance insights
        insights = self.CreatePerformanceInsights(results, performance_score)
        
        # Recommendations section
        recommendations = self.CreateRecommendationsSection(results)
        
        # Add all sections to results
        sections = [
            ft.Divider(height=20),
            
            # Performance score and metrics
            ft.Column([
                ft.Row([
                    score_card,
                    ft.VerticalDivider(),
                    ft.Column([
                        ft.Text("Key Metrics", size=16, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                        metrics_row
                    ], expand=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=10),
                additional_metrics_row,
                ft.Divider(height=10),
                ft.Text("Resources Analysis", size=16, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                resources_row,
                ft.Divider(height=10),
                ft.Text("Best Practices", size=16, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                best_row
            ]),
            
            ft.Divider(height=20),
        ]
        
        # Add advanced metrics if available
        if advanced_metrics:
            sections.extend([
                ft.Text("Advanced Metrics", size=18, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                advanced_metrics,
                ft.Divider(height=20)
            ])
            
            # Add performance grade if available
            if grade_card:
                sections.extend([
                    ft.Row([
                        grade_card,
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Content Analysis", size=16, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                                ft.Text(f"Images: {results.get('content_analysis', {}).get('img_count', 0)}", size=12, font_family="Iransans-Regular"),
                                ft.Text(f"Links: {results.get('content_analysis', {}).get('link_count', 0)}", size=12, font_family="Iransans-Regular"),
                                ft.Text(f"Scripts: {results.get('content_analysis', {}).get('script_count', 0)}", size=12, font_family="Iransans-Regular"),
                            ]),
                            bgcolor=ft.Colors.BLUE_50,
                            border_radius=ft.border_radius.all(8),
                            padding=10,
                            width=200
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Divider(height=20)
                ])
        
        # Add pie chart
        sections.extend([
            ft.Text("Performance Distribution", size=18, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
            pie_chart,
            ft.Divider(height=20),
            
            # Detailed metrics
            detailed_metrics,
            ft.Divider(height=20)
        ])
        
        # Add cache details if available
        if cache_details:
            sections.extend([
                cache_details,
                ft.Divider(height=20)
            ])
        
        # Add security analysis if available
        if 'security_headers' in results:
            security_section = ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"Security Analysis - Score: {results['security_headers']['score']}/6 ({results['security_headers']['grade']})",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        font_family="Iransans-Bold"
                    ),
                    ft.Divider(),
                    self.CreateDetailRow("HSTS", results['security_headers']['https']),
                    self.CreateDetailRow("X-Frame-Options", results['security_headers']['x_frame_options']),
                    self.CreateDetailRow("X-Content-Type-Options", results['security_headers']['x_content_type']),
                    self.CreateDetailRow("X-XSS-Protection", results['security_headers']['x_xss_protection']),
                    self.CreateDetailRow("CSP", results['security_headers']['content_security_policy']),
                    self.CreateDetailRow("Referrer Policy", results['security_headers']['referrer_policy']),
                ]),
                bgcolor=ft.Colors.RED_50,
                border_radius=ft.border_radius.all(10),
                padding=15
            )
            sections.extend([
                security_section,
                ft.Divider(height=20)
            ])
        
        # Add performance insights and recommendations
        sections.extend([
            # Performance insights
            insights,
            ft.Divider(height=20),
            
            # Recommendations
            recommendations
        ])
        
        self.results_container.content.controls.extend(sections)
        
        self.page.update()
    
    def CreateMetricCard(self, title, value, icon):
        """
        Create a metric card with icon and value.
        
        Args:
            title (str): Card title
            value (str): Card value
            icon: Icon to display
            
        Returns:
            ft.Container: Metric card container
        """
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=25, color=ft.Colors.CYAN),
                ft.Text(title, size=11, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                ft.Text(str(value), size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_700, font_family="Iransans-Bold", text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(8),
            padding=12,
            border=ft.border.all(1, ft.Colors.CYAN_200),
            width=120,
            height=100
        )
    
    def CreateDetailRow(self, label, value):
        """
        Create a detail row with label and value.
        
        Args:
            label (str): Row label
            value (str): Row value
            
        Returns:
            ft.Row: Detail row
        """
        return ft.Row([
            ft.Text(f"{label}:", size=14, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold", width=120),
            ft.Text(str(value), size=14, font_family="Iransans-Regular", expand=True)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def CreatePerformancePieChart(self, results):
        """
        Create a pie chart showing performance breakdown.
        
        Args:
            results (dict): Analysis results
            
        Returns:
            ft.Container: Pie chart container
        """
        # Calculate performance categories
        response_time = results['response_time']
        content_size = results['content_size']
        
        # Performance categories
        categories = []
        
        # Response time category
        if response_time < 200:
            categories.append(("Excellent Response Time", 40, ft.Colors.GREEN))
        elif response_time < 1000:
            categories.append(("Good Response Time", 30, ft.Colors.ORANGE))
        else:
            categories.append(("Poor Response Time", 20, ft.Colors.RED))
        
        # Content size category
        if content_size < 1024 * 1024:  # < 1MB
            categories.append(("Appropriate Size", 30, ft.Colors.GREEN))
        elif content_size < 5 * 1024 * 1024:  # < 5MB
            categories.append(("Average Size", 20, ft.Colors.ORANGE))
        else:
            categories.append(("Large Size", 10, ft.Colors.RED))
        
        # Create pie chart representation
        pie_sections = []
        for name, percentage, color in categories:
            pie_sections.append(
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            width=20,
                            height=20,
                            bgcolor=color,
                            border_radius=ft.border_radius.all(10)
                        ),
                        ft.Text(f"{name}: {percentage}%", size=12, font_family="Iransans-Regular")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=120
                )
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Performance Distribution", size=16, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                ft.Row(pie_sections, alignment=ft.MainAxisAlignment.SPACE_AROUND)
            ]),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            padding=20,
            border=ft.border.all(1, ft.Colors.CYAN_200)
        )
    
    def CreatePerformanceInsights(self, results, score):
        """
        Create performance insights section.
        
        Args:
            results (dict): Analysis results
            score (int): Performance score
            
        Returns:
            ft.Container: Insights container
        """
        insights = []
        
        # Response time insights
        if results['response_time'] < 200:
            insights.append("✅ Excellent response time - server is optimized")
        elif results['response_time'] < 1000:
            insights.append("⚠️ Average response time - server improvement recommended")
        else:
            insights.append("❌ Poor response time - urgent optimization needed")
        
        # Content size insights
        if results['content_size'] < 1024 * 1024:
            insights.append("✅ Content size is appropriate")
        elif results['content_size'] < 5 * 1024 * 1024:
            insights.append("⚠️ Average content size - compression recommended")
        else:
            insights.append("❌ Large content size - optimization essential")
        
        # Status code insights
        if results['status_code'] == 200:
            insights.append("✅ Server responds correctly")
        else:
            insights.append(f"⚠️ Status code {results['status_code']} - server check recommended")
        
        insight_items = []
        for insight in insights:
            insight_items.append(
                ft.Text(insight, size=14, font_family="Iransans-Regular")
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Performance Insights", size=18, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                ft.Divider(),
                *insight_items
            ]),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=ft.border_radius.all(10),
            padding=15,
            border=ft.border.all(1, ft.Colors.BLUE_200)
        )
    
    def CreateRecommendationsSection(self, results):
        """
        Create detailed recommendations section.
        
        Args:
            results (dict): Analysis results
            
        Returns:
            ft.Container: Recommendations container
        """
        recommendations = self.GetDetailedRecommendations(results)
        
        rec_items = []
        for i, rec in enumerate(recommendations, 1):
            rec_items.append(
                ft.Row([
                    ft.Text(f"{i}.", size=14, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold", width=30),
                    ft.Text(rec, size=14, font_family="Iransans-Regular", expand=True)
                ])
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Optimization Recommendations", size=18, weight=ft.FontWeight.BOLD, font_family="Iransans-Bold"),
                ft.Divider(),
                *rec_items
            ]),
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=ft.border_radius.all(10),
            padding=15,
            border=ft.border.all(1, ft.Colors.ORANGE_200)
        )
    
    def GetPerformanceLabel(self, score):
        """
        Get performance label based on score.
        
        Args:
            score (int): Performance score
            
        Returns:
            str: Performance label
        """
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Average"
        elif score >= 60:
            return "Poor"
        else:
            return "Very Poor"
    
    def GetCurrentDateTime(self):
        """
        Get current date and time.
        
        Returns:
            str: Formatted date and time
        """
        from datetime import datetime
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    def GetDetailedRecommendations(self, results):
        """
        Get detailed recommendations based on analysis results.
        
        Args:
            results (dict): Analysis results
            
        Returns:
            list: List of detailed recommendations
        """
        recommendations = []
        
        # Response time recommendations
        if results['response_time'] > 2000:
            recommendations.append("Use CDN to reduce response time")
            recommendations.append("Optimize server code and database")
            recommendations.append("Enable Gzip compression")
        
        # Content size recommendations
        if results['content_size'] > 1024 * 1024:
            recommendations.append("Compress images with WebP format")
            recommendations.append("Remove unnecessary CSS and JavaScript code")
            recommendations.append("Use lazy loading for images")
        
        # General recommendations
        recommendations.append("Enable browser cache")
        recommendations.append("Use HTTP/2 for better performance")
        recommendations.append("Optimize JavaScript and CSS code")
        
        # Server-specific recommendations
        if "nginx" in results['server'].lower():
            recommendations.append("Configure Nginx optimization")
        elif "apache" in results['server'].lower():
            recommendations.append("Configure Apache optimization")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def OnToggleAdvanced(self, e):
        """Toggle advanced options visibility."""
        self.advanced_options.visible = not self.advanced_options.visible
        self.page.update()
    
    def OnMultipleTestChange(self, e):
        """Handle multiple test checkbox change."""
        self.multiple_test = e.control.value
    
    def OnDeepTestChange(self, e):
        """Handle deep test checkbox change."""
        self.deep_test = e.control.value
    
    def OnMobileTestChange(self, e):
        """Handle mobile test checkbox change."""
        self.mobile_test = e.control.value
    
    def OnTestCountChange(self, e):
        """Handle test count slider change."""
        self.test_count = int(e.control.value)

    def OnBrowserTestChange(self, e):
        """Handle headless browser test toggle."""
        self.browser_test = e.control.value
    
    def CalculatePerformanceScore(self, response_time):
        """
        Calculate performance score based on response time.
        
        Args:
            response_time (float): Response time in milliseconds
            
        Returns:
            int: Performance score (0-100)
        """
        if response_time < 200:
            return 100
        elif response_time < 500:
            return 90
        elif response_time < 1000:
            return 80
        elif response_time < 2000:
            return 70
        elif response_time < 3000:
            return 60
        else:
            return 50
    
    def GetPerformanceColor(self, score):
        """
        Get color based on performance score.
        
        Args:
            score (int): Performance score
            
        Returns:
            str: Color string
        """
        if score >= 90:
            return ft.Colors.GREEN
        elif score >= 70:
            return ft.Colors.ORANGE
        else:
            return ft.Colors.RED
    
    def FormatBytes(self, bytes_size):
        """
        Format bytes to human readable format.
        
        Args:
            bytes_size (int): Size in bytes
            
        Returns:
            str: Formatted size string
        """
        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.1f} KB"
        else:
            return f"{bytes_size / (1024 * 1024):.1f} MB"
    
    def GetRecommendations(self, results):
        """
        Get performance recommendations based on analysis results.
        
        Args:
            results (dict): Analysis results
            
        Returns:
            list: List of recommendation strings
        """
        recommendations = []
        
        if results['response_time'] > 2000:
            recommendations.append("Response time is high. Consider server optimization.")
        
        if results['content_size'] > 1024 * 1024:  # > 1MB
            recommendations.append("Page size is large. Consider compressing images and code.")
        
        if results['status_code'] != 200:
            recommendations.append("Status code is not 200. Check server issues.")
        
        if not recommendations:
            recommendations.append("Website performance is good! 🎉")
        
        return recommendations
