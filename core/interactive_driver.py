"""交互式驱动 - 支持逐步执行和会话状态管理"""
from playwright.sync_api import sync_playwright
import requests
import os
import json
from core.session_manager import SessionManager

class InteractiveDriver:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = InteractiveDriver()
        return cls._instance
    
    def __init__(self):
        self.session = SessionManager()
    
    def _ensure_browser(self):
        """确保浏览器已启动"""
        if not self.session.browser:
            self.session.playwright = sync_playwright().start()
            self.session.browser = self.session.playwright.chromium.launch(headless=False)
            self.session.page = self.session.browser.new_page()
    
    def execute(self, command):
        """执行单个命令"""
        try:
            action = command.get('action')
            
            # === 浏览器操作 ===
            if action == 'navigate':
                self._ensure_browser()
                url = command.get('url')
                self.session.page.goto(url)
                return {"status": "success", "message": f"已导航到 {url}"}
            
            elif action == 'click':
                selector = command.get('selector')
                self.session.page.evaluate(f'document.querySelector("{selector}").click()')
                return {"status": "success", "message": f"已点击 {selector}"}
            
            elif action == 'type':
                selector = command.get('selector')
                text = command.get('text')
                self.session.page.evaluate(f'''
                    const el = document.querySelector("{selector}");
                    el.value = "{text}";
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ''')
                return {"status": "success", "message": "已输入文本"}
            
            elif action == 'wait':
                selector = command.get('selector')
                timeout = command.get('timeout', 5000)
                self.session.page.wait_for_selector(selector, timeout=timeout, state='attached')
                return {"status": "success", "message": "元素已出现"}
            
            elif action == 'screenshot':
                path = command.get('path')
                os.makedirs(os.path.dirname(path), exist_ok=True)
                self.session.page.screenshot(path=path, full_page=True)
                return {"status": "success", "path": path}
            
            elif action == 'get_text':
                selector = command.get('selector')
                text = self.session.page.evaluate(f'document.querySelector("{selector}").innerText')
                return {"status": "success", "text": text}
            
            elif action == 'get_url':
                url = self.session.page.url
                return {"status": "success", "url": url}
            
            # === REST API 操作 ===
            elif action == 'api_request':
                method = command.get('method', 'GET').upper()
                url = command.get('url')
                data = command.get('data')
                
                # 使用会话中的认证信息
                headers = self.session.headers.copy()
                cookies = self.session.cookies
                
                response = requests.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers,
                    cookies=cookies
                )
                
                return {
                    "status": "success",
                    "status_code": response.status_code,
                    "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            
            # === 会话管理操作 ===
            elif action == 'set_jwt':
                token = command.get('token')
                self.session.set_jwt(token)
                return {"status": "success", "message": "JWT token 已设置"}
            
            elif action == 'set_cookie':
                name = command.get('name')
                value = command.get('value')
                self.session.set_cookie(name, value)
                return {"status": "success", "message": f"Cookie {name} 已设置"}
            
            elif action == 'set_header':
                name = command.get('name')
                value = command.get('value')
                self.session.set_header(name, value)
                return {"status": "success", "message": f"Header {name} 已设置"}
            
            elif action == 'set_variable':
                name = command.get('name')
                value = command.get('value')
                self.session.set_variable(name, value)
                return {"status": "success", "message": f"变量 {name} 已设置"}
            
            elif action == 'get_variable':
                name = command.get('name')
                value = self.session.get_variable(name)
                return {"status": "success", "value": value}
            
            elif action == 'get_state':
                state = self.session.get_state()
                return {"status": "success", "state": state}
            
            elif action == 'save_state':
                path = command.get('path', 'session_state.json')
                self.session.save_state(path)
                return {"status": "success", "message": f"会话状态已保存到 {path}"}
            
            elif action == 'load_state':
                path = command.get('path', 'session_state.json')
                self.session.load_state(path)
                return {"status": "success", "message": f"会话状态已从 {path} 加载"}
            
            elif action == 'close':
                self.close()
                return {"status": "success", "message": "会话已关闭"}
            
            else:
                return {"status": "error", "message": f"未知操作: {action}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def close(self):
        """关闭浏览器和清理会话"""
        if self.session.browser:
            self.session.browser.close()
            self.session.playwright.stop()
        self.session = SessionManager()
        InteractiveDriver._instance = None
