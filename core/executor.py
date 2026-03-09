"""执行引擎"""
import yaml
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.session import TestSession
from core.data_loader import DataLoader
from drivers.rest_driver import RESTDriver
from drivers.ui_driver import UIDriver

# 可选导入 mobile driver
try:
    from drivers.mobile_driver import MobileDriver
    MOBILE_AVAILABLE = True
except ImportError:
    MOBILE_AVAILABLE = False

class Executor:
    def __init__(self):
        self.session = TestSession()
        self.data_loader = DataLoader()
        self.drivers = {
            'rest': RESTDriver(self.session),
            'ui': UIDriver(self.session),
        }
        if MOBILE_AVAILABLE:
            self.drivers['mobile'] = MobileDriver()
    
    def execute(self, dsl_file):
        """执行 DSL 文件"""
        with open(dsl_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print(f"执行测试: {config.get('name', 'Unnamed')}")
        print(f"描述: {config.get('description', 'No description')}")
        
        steps = config.get('steps', [])
        for i, step in enumerate(steps, 1):
            action = step.get('action')
            print(f"\n步骤 {i}: {action}")
            
            # 根据 action 类型选择驱动
            if action in ['navigate', 'click', 'type', 'wait', 'screenshot']:
                driver = self.drivers['ui']
            elif action in ['get', 'post', 'put', 'delete']:
                driver = self.drivers['rest']
            elif action in ['tap', 'swipe'] and MOBILE_AVAILABLE:
                driver = self.drivers['mobile']
            else:
                print(f"未知操作: {action}")
                continue
            
            # 执行步骤
            try:
                driver.execute_step(step)
                print(f"✓ 步骤 {i} 完成")
            except Exception as e:
                print(f"✗ 步骤 {i} 失败: {e}")
                raise
        
        print("\n测试执行完成!")
        
        # 关闭驱动
        if 'ui' in self.drivers:
            self.drivers['ui'].close()
