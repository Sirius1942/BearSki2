"""测试编排引擎"""
import json
from typing import List, Dict, Any
from datetime import datetime


class TestOrchestrator:
    def __init__(self):
        self.workflows = {}
    
    def create_workflow(self, name: str, steps: List[Dict[str, Any]]):
        self.workflows[name] = {'name': name, 'steps': steps, 'created_at': datetime.now().isoformat()}
    
    def execute_workflow(self, name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if name not in self.workflows:
            raise ValueError(f"Workflow '{name}' not found")
        
        workflow = self.workflows[name]
        context = context or {}
        results = []
        
        for i, step in enumerate(workflow['steps']):
            if 'condition' in step and not self._eval_condition(step['condition'], context):
                results.append({'step': i+1, 'action': step['action'], 'status': 'skipped'})
                continue
            
            try:
                result = self._execute_step(step, context)
                results.append({'step': i+1, 'action': step['action'], 'status': 'passed', 'result': result})
                if 'output' in step:
                    context[step['output']] = result
            except Exception as e:
                results.append({'step': i+1, 'action': step['action'], 'status': 'failed', 'error': str(e)})
                if step.get('on_fail') == 'stop':
                    break
        
        return {
            'workflow': name,
            'total_steps': len(workflow['steps']),
            'passed': sum(1 for r in results if r['status'] == 'passed'),
            'failed': sum(1 for r in results if r['status'] == 'failed'),
            'results': results,
            'context': context
        }
    
    def _eval_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        try:
            return eval(condition, {"__builtins__": {}}, context)
        except:
            return False
    
    def _execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Any:
        action = step['action']
        params = step.get('params', {})
        
        for key, value in params.items():
            if isinstance(value, str) and value.startswith('$'):
                params[key] = context.get(value[1:], value)
        
        if action == 'api_call':
            return {'status': 200, 'data': params}
        elif action == 'assert':
            if not params.get('condition', True):
                raise AssertionError(params.get('message', 'Assertion failed'))
            return True
        return f"Executed {action}"
    
    def save_workflow(self, name: str, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(self.workflows[name], f, indent=2)
    
    def load_workflow(self, filepath: str) -> str:
        with open(filepath, 'r') as f:
            workflow = json.load(f)
        name = workflow['name']
        self.workflows[name] = workflow
        return name
