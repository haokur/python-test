import signal
import subprocess

# 执行系统命令
# command = "ls"
# try:
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     if result.stderr:
#         print("错误输出:")
#         print(result.stderr)
#     else:
#         print("命令输出:")
#         print(result.stdout)
# except Exception as e:
#     print(f"执行命令时出错: {e}")


# import subprocess
# import sys


# def handle_exit(signal_num, frame):
#     sys.exit(0)


# signal.signal(signal.SIGINT, handle_exit)
# signal.signal(signal.SIGTERM, handle_exit)

# # 执行系统命令
# command = "ping baidu.com"
# try:
#     subprocess.run(command, shell=True)
# except Exception as e:
#     print(f"执行命令时出错: {e}")
import os
import platform

system_name = platform.system()
is_windows_system = system_name == "Windows"
is_mac_system = system_name == "Darwin"
is_linux_system = system_name == "Linux"


def run_cmd_by_new_windows(cmd):
    if is_windows_system:
        print("打开新窗口运行命令")
    elif is_mac_system:
        # AppleScript 命令
        script = f"""
        tell application "Terminal"
            activate
            do script "{cmd}"
        end tell
        """
        os.system(f"osascript -e '{script}'")
    else:
        print("非windows系统")


run_cmd_by_new_windows("ls")
