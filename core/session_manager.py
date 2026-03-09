"""会话管理器 - 保持浏览器和 API 认证状态"""
import json
import os

class SessionManager:
    """管理测试会话的所有状态"""
    
    def __init__(self):
        # 浏览器状态
        self.browser = None
        self.page = None
        self.playwright = None
        
        # REST API 状态
        self.jwt_token = None
        self.cookies = {}
        self.headers = {}
        self.base_url = None
        
        # 会话变量（用户自定义）
        self.variables = {}
    
    def set_jwt(self, token):
        """设置 JWT token"""
        self.jwt_token = token
        self.headers['Authorization'] = f'Bearer {token}'
    
    def set_cookie(self, name, value):
        """设置 cookie"""
        self.cookies[name] = value
    
    def set_header(self, name, value):
        """设置请求头"""
        self.headers[name] = value
    
    def set_variable(self, name, value):
        """设置会话变量"""
        self.variables[name] = value
    
    def get_variable(self, name):
        """获取会话变量"""
        return self.variables.get(name)
    
    def get_state(self):
        """获取当前会话状态"""
        return {
            "browser_active": self.browser is not None,
            "jwt_token": self.jwt_token,
            "cookies": self.cookies,
            "headers": self.headers,
            "variables": self.variables,
            "base_url": self.base_url
        }
    
    def save_state(self, path):
        """保存会话状态到文件"""
        state = {
            "jwt_token": self.jwt_token,
            "cookies": self.cookies,
            "headers": self.headers,
            "variables": self.variables,
            "base_url": self.base_url
        }
        dir_path = os.path.dirname(path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, path):
        """从文件加载会话状态"""
        with open(path, 'r') as f:
            state = json.load(f)
        self.jwt_token = state.get('jwt_token')
        self.cookies = state.get('cookies', {})
        self.headers = state.get('headers', {})
        self.variables = state.get('variables', {})
        self.base_url = state.get('base_url')
