"""BearSki 2.0 主程序"""
import sys
from core.executor import Executor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python main.py <dsl_file>")
        sys.exit(1)
    
    dsl_file = sys.argv[1]
    executor = Executor()
    executor.execute(dsl_file)
