from core.orchestrator import TestOrchestrator

orchestrator = TestOrchestrator()

# 创建工作流
orchestrator.create_workflow('user_journey', [
    {'action': 'api_call', 'params': {'endpoint': '/login', 'user': 'test'}, 'output': 'token'},
    {'action': 'api_call', 'params': {'endpoint': '/profile', 'token': '$token'}, 'output': 'profile'},
    {'action': 'assert', 'params': {'condition': True, 'message': 'Profile loaded'}, 'condition': 'profile is not None'},
    {'action': 'api_call', 'params': {'endpoint': '/logout'}, 'on_fail': 'stop'}
])

# 执行工作流
result = orchestrator.execute_workflow('user_journey')

print(f"工作流: {result['workflow']}")
print(f"总步骤: {result['total_steps']}")
print(f"通过: {result['passed']}, 失败: {result['failed']}")
print(f"\n步骤详情:")
for r in result['results']:
    print(f"  步骤{r['step']}: {r['action']} - {r['status']}")

# 保存工作流
orchestrator.save_workflow('user_journey', 'workflows/user_journey.json')
print("\n✅ 工作流已保存")
