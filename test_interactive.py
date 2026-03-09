"""交互式模式测试示例"""
from core.interactive_driver import InteractiveDriver
import json

# 获取驱动实例
driver = InteractiveDriver.get_instance()

# 步骤 1: 打开百度
print("步骤 1: 打开百度")
result = driver.execute({"action": "navigate", "url": "https://www.baidu.com"})
print(json.dumps(result, ensure_ascii=False))

# 步骤 2: 截图
print("\n步骤 2: 截图首页")
result = driver.execute({"action": "screenshot", "path": "screenshots/interactive_step1.png"})
print(json.dumps(result, ensure_ascii=False))

# 步骤 3: 输入搜索词
print("\n步骤 3: 输入搜索词")
result = driver.execute({"action": "type", "selector": "input#kw", "text": "BearSki 自动化"})
print(json.dumps(result, ensure_ascii=False))

# 步骤 4: 点击搜索
print("\n步骤 4: 点击搜索")
result = driver.execute({"action": "click", "selector": "input#su"})
print(json.dumps(result, ensure_ascii=False))

# 步骤 5: 等待结果
print("\n步骤 5: 等待结果")
result = driver.execute({"action": "wait", "selector": "div#content_left"})
print(json.dumps(result, ensure_ascii=False))

# 步骤 6: 截图结果
print("\n步骤 6: 截图结果")
result = driver.execute({"action": "screenshot", "path": "screenshots/interactive_step2.png"})
print(json.dumps(result, ensure_ascii=False))

# 关闭
print("\n关闭浏览器")
driver.close()
