"""
BearSki 2.0 - Mobile Driver
移动端自动化驱动（基于 Appium）
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time


class MobileDriver:
    """移动端驱动"""
    
    def __init__(self):
        self.driver = None
        
    def start_app(self, package: str, activity: str = None, **kwargs):
        """启动 App"""
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.app_package = package
        if activity:
            options.app_activity = activity
            
        # Appium Server 地址
        appium_server = kwargs.get('appium_server', 'http://localhost:4723')
        
        self.driver = webdriver.Remote(appium_server, options=options)
        time.sleep(2)  # 等待启动
        return True
        
    def click(self, locator: str, **kwargs):
        """点击元素"""
        element = self._find_element(locator)
        element.click()
        return True
        
    def input(self, locator: str, text: str, **kwargs):
        """输入文本"""
        element = self._find_element(locator)
        element.clear()
        element.send_keys(text)
        return True
        
    def swipe(self, direction: str, **kwargs):
        """滑动"""
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']
        
        if direction == 'up':
            self.driver.swipe(width/2, height*0.8, width/2, height*0.2, 500)
        elif direction == 'down':
            self.driver.swipe(width/2, height*0.2, width/2, height*0.8, 500)
        elif direction == 'left':
            self.driver.swipe(width*0.8, height/2, width*0.2, height/2, 500)
        elif direction == 'right':
            self.driver.swipe(width*0.2, height/2, width*0.8, height/2, 500)
        return True
        
    def screenshot(self, path: str, **kwargs):
        """截图"""
        self.driver.save_screenshot(path)
        return True
        
    def _find_element(self, locator: str):
        """查找元素"""
        if locator.startswith('id='):
            element_id = locator.replace('id=', '')
            return self.driver.find_element(AppiumBy.ID, element_id)
        elif locator.startswith('xpath='):
            xpath = locator.replace('xpath=', '')
            return self.driver.find_element(AppiumBy.XPATH, xpath)
        elif locator.startswith('text='):
            text = locator.replace('text=', '')
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
                f'new UiSelector().text("{text}")')
        else:
            # 默认使用 ID
            return self.driver.find_element(AppiumBy.ID, locator)
            
    def close(self):
        """关闭驱动"""
        if self.driver:
            self.driver.quit()
        return True
