"""会话状态管理测试示例"""
from core.interactive_driver import InteractiveDriver
import json

driver = InteractiveDriver.get_instance()

print("=== 场景 1: Web 登录并保存会话 ===\n")

# 步骤 1: 打开登录页
result = driver.execute({"action": "navigate", "url": "https://www.baidu.com"})
print(f"1. {result['message']}")

# 步骤 2: 保存用户名到会话变量
result = driver.execute({"action": "set_variable", "name": "username", "value": "testuser"})
print(f"2. {result['message']}")

# 步骤 3: 模拟获取 JWT token
result = driver.execute({"action": "set_jwt", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."})
print(f"3. {result['message']}")

# 步骤 4: 设置自定义 header
result = driver.execute({"action": "set_header", "name": "X-Client-Version", "value": "1.0.0"})
print(f"4. {result['message']}")

# 步骤 5: 查看当前会话状态
result = driver.execute({"action": "get_state"})
print(f"\n5. 当前会话状态:")
print(json.dumps(result['state'], indent=2, ensure_ascii=False))

# 步骤 6: 保存会话状态
result = driver.execute({"action": "save_state", "path": "session_state.json"})
print(f"\n6. {result['message']}")

print("\n=== 场景 2: 恢复会话并继续操作 ===\n")

# 关闭当前会话
driver.close()

# 创建新实例
driver = InteractiveDriver.get_instance()

# 步骤 7: 加载之前保存的会话
result = driver.execute({"action": "load_state", "path": "session_state.json"})
print(f"7. {result['message']}")

# 步骤 8: 获取之前保存的变量
result = driver.execute({"action": "get_variable", "name": "username"})
print(f"8. 恢复的用户名: {result['value']}")

# 步骤 9: 查看恢复后的状态
result = driver.execute({"action": "get_state"})
print(f"\n9. 恢复后的会话状态:")
print(json.dumps(result['state'], indent=2, ensure_ascii=False))

print("\n✅ 会话状态管理测试完成！")
