"""UI 驱动 - Playwright"""
from playwright.sync_api import sync_playwright
import os
import time

class UIDriver:
    def __init__(self, session):
        self.session = session
        if not self.session.ui_browser:
            self.playwright = sync_playwright().start()
            self.session.ui_browser = self.playwright.chromium.launch(headless=False)
            self.page = self.session.ui_browser.new_page()
    
    def execute_step(self, step):
        """执行单个步骤"""
        action = step.get('action')
        
        if action == 'navigate':
            url = step.get('url')
            print(f"  → 打开页面: {url}")
            self.page.goto(url)
            time.sleep(2)
        
        elif action == 'click':
            selector = step.get('selector')
            print(f"  → 点击: {selector}")
            # 使用 JavaScript 强制点击
            self.page.evaluate(f'document.querySelector("{selector}").click()')
            time.sleep(1)
        
        elif action == 'type':
            selector = step.get('selector')
            text = step.get('text')
            print(f"  → 输入: {text}")
            # 使用 JavaScript 直接设置值
            self.page.evaluate(f'''
                const el = document.querySelector("{selector}");
                el.value = "{text}";
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ''')
            time.sleep(1)
        
        elif action == 'wait':
            selector = step.get('selector')
            timeout = step.get('timeout', 5000)
            print(f"  → 等待元素: {selector}")
            self.page.wait_for_selector(selector, timeout=timeout, state='attached')
        
        elif action == 'screenshot':
            path = step.get('path')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.page.screenshot(path=path, full_page=True)
            print(f"  → 截图保存: {path}")
    
    def close(self):
        """关闭浏览器"""
        if self.session.ui_browser:
            self.session.ui_browser.close()
            self.playwright.stop()
