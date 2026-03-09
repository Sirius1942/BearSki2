"""交互式测试入口"""
import sys
import json
from core.interactive_driver import InteractiveDriver

if __name__ == "__main__":
    driver = InteractiveDriver.get_instance()
    
    if len(sys.argv) > 1:
        # 命令行模式：执行单个命令
        command = json.loads(sys.argv[1])
        result = driver.execute(command)
        print(json.dumps(result, ensure_ascii=False))
    else:
        # REPL 模式：交互式输入
        print("BearSki 2.0 交互式测试模式")
        print("输入 JSON 命令，输入 'exit' 退出")
        print()
        
        while True:
            try:
                line = input(">>> ")
                if line.strip().lower() == 'exit':
                    driver.close()
                    break
                
                command = json.loads(line)
                result = driver.execute(command)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except KeyboardInterrupt:
                print("\n退出")
                driver.close()
                break
            except Exception as e:
                print(f"错误: {e}")
