import argparse

parser = argparse.ArgumentParser()
# 添加位置参数
# parser.add_argument('echo', help='echo command help information')
# 可选参数，运行时不添加该参数则为True, 添加该参数则为False
# action : store_true:出现则存储的时True, count：计算该参数出现的次数
# parser.add_argument('--op', help='op help information', action='store_false')
# parser.add_argument('-t','--test', action='count')

# nargs='+', nargs='*' 表示-n后的是n的参数而不是位置参数，如-n 1 2 3，这里解析n=[1,2,3]而不会认为1，2，3是位置参数
# parser.add_argument('-n', nargs='+')

# 允许我们添加彼此相冲的参数，即这两个参数不能同时出现
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

# argparse 模块的输出例如它的帮助文本和错误消息都可以通过 gettext 模块实现翻译

args = parser.parse_args()

