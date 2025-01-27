import pexpect
import sys

class Logger:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        # 将 bytes 转为 str
        text = data.decode('utf-8')
        for stream in self.streams:
            stream.write(text)

    def flush(self):
        for stream in self.streams:
            stream.flush()

# 测试sudo执行然后输入密码
def run_get_pwd(log_file_path='output.log'):
  with open(log_file_path, 'w') as log_file:
    child = pexpect.spawn('sudo pwd')
    child.logfile = Logger(sys.stdout, log_file)  # 同时输出到屏幕和日志

    child.expect('Password:')
    child.sendline('123456')

    # 等待子进程完成（一定不能少）
    # 缺少这一行，则不会等child执行完，就退出程序
    child.expect(pexpect.EOF)

def run_connect_ssh(log_file_path='output.log'):
  with open(log_file_path, 'w') as log_file:
    child = pexpect.spawn("ssh root@127.0.0.1 -p 8080")
    child.logfile = Logger(sys.stdout, log_file)  # 同时输出到屏幕和日志

    # 可以是全部打印，也可以是简略的最后几个字符如"password:"
    # child.expect("haokur@xxxxxxxx's password:")
    child.expect("password:")
    child.sendline('123456')

    child.expect(pexpect.EOF)

def run_ping(log_file_path='output.log'):
  with open(log_file_path, 'w') as log_file:
    child = pexpect.spawn("ping baidu.com")
    child.logfile = Logger(sys.stdout, log_file)  # 同时输出到屏幕和日志

    child.expect(pexpect.EOF)

# 将命令，输出日志，匹配问题，匹配答案，封装成一个通用方法
def run_command(command, log_file_path, expect_patterns=None, responses=None):
  """
  通用命令执行函数，支持多个匹配条件和响应。

  :param command: 要执行的命令
  :param log_file_path: 日志文件路径
  :param expect_patterns: 要匹配的多个条件（列表）
  :param responses: 对应每个条件的响应（列表）
  """
  if expect_patterns is None:
    expect_patterns = []
  if responses is None:
    responses = []

  try:
    with open(log_file_path, 'w') as log_file:
      child = pexpect.spawn(command)
      child.logfile = Logger(sys.stdout, log_file)  # 同时输出到屏幕和日志

      # 循环处理匹配项
      while True:
        index = child.expect(expect_patterns + [pexpect.EOF, pexpect.TIMEOUT])

        # 匹配到 EOF，表示子进程结束
        if index == len(expect_patterns):
          print("\n子进程已完成。")
          break

        # 匹配到 TIMEOUT
        elif index == len(expect_patterns) + 1:
          print("\n匹配超时。")
          break

        # 对应的匹配项
        else:
          if index < len(responses):
            child.sendline(responses[index])  # 发送对应的响应
          else:
            print(f"未定义的匹配条件: {expect_patterns[index]}")

  except Exception as e:
    print(f"发生错误: {e}")
  finally:
    if 'child' in locals() and child.isalive():
      child.terminate()
    print("清理完成，程序已退出。")

def program_entry_run():
  # run_get_pwd()
  # run_connect_ssh()
  # run_ping()
  run_command("sudo ls","output.log",["Password:"],["123456"])

try:
  program_entry_run()
except KeyboardInterrupt:
  print("\n程序已被用户中断，正在退出...")
except Exception as e:
  print(f"发生错误: {e}")
finally:
  print("程序退出")
