# 最简单的 try-expect-finally
# def run_main():
#     input("按任意键盘退出~")


# try:
#     run_main()
# except KeyboardInterrupt:
#     print("程序被用户手动中断")
# finally:
#     print("程序结束统一处理")


# 使用信号处理
import signal
import sys


def handle_exit(signum,frame):
    print("\n收到信号{}，程序退出...".format(signum))
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)  # 捕获 Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # 捕获终止信号

input("使用ctrl+C退出程序!\n")
