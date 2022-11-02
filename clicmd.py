#!/opt/anaconda3/bin/python
#coding = utf-8
from ast import keyword
import cmd
from logging.handlers import BaseRotatingHandler
import sys
import readline
import rlcompleter

from cat_cmd import CatArg

MAMMAL_KEY = {'MAMMAL': ('cat', 'dog', 'pig')}
MAMMAL_CAT_KEY = {'MAMMAL_CAT': ('color=', 'size=', 'color_a=')}
MAMMAL_DOG_KEY = {'MAMMAL_DOG': ('color', 'size')}
MAMMAL_PIG_KEY = {'MAMMAL_PIG': ('color', 'size')}

COMPLETE_MAMMAL = dict(**MAMMAL_KEY, **MAMMAL_CAT_KEY, **MAMMAL_DOG_KEY, **MAMMAL_PIG_KEY)


class Cli(cmd.Cmd):
    
    def __init__(self):
        readline.parse_and_bind('tab:complete')
        super(Cli, self).__init__()
        self.intro = "Welcome to Bobibalabala's Cmdline system"
        self.prompt = "<Bobi>"
        self.last_key = ''
        
    def onecmd(self, line):
        return super().onecmd(line)

    def precmd(self, line):
        if line:
            line_l = line.split()
            if len(line_l) == 1 and line_l[0] in ('q','quit','exit'):
                self.do_quit()
            else:
                return line
        else:
            return line      
        
    def do_mammal(self, line: str):
        '''mammal'''
        # print(arg,type(arg))
        if line.startswith(('-h','--help')):
            self.help_mammal()
            return
        CatArg(line)

    def complete_mammal(self, text, line, begidx, endidx):
        return self._complete(text, line, begidx, endidx, cmddict=COMPLETE_MAMMAL)

    def help_mammal(self):
        info = """mammal command:
                cat :  color  size
                dog :  color  size
                pig :  color  size
                """
        print(info)

    def do_birds(self, line):
        print('birds')

    def do_quit(self):
        exit()

    def _complete(self, text, line, begidx, endidx, cmddict=None):
        """自己写的用于命令行补全的函数"""
        ret_list = []  #用来收集返回的值
        if begidx == endidx:  #如果这两个值相等，则说明遇到了空格，且begidx就是空格的位置
            index = line.find('=') #如果是关键字参数，那么就在上一个容器中返回补全值
            if index == -1: #如果没找到=号，说明没有关键字参数
                key = line.rstrip().replace(' ', '_').upper()
                ret_list = cmddict[key]
                return ret_list
            else:
                left_part = line[:index].split() 
                left_part.remove(left_part[-1])
                key = '_'.join(left_part).upper()
                ret_list = list(cmddict[key]) #获得关键字参数补全列表
                orginal_line_list = line.split()
                for item in orginal_line_list:
                    if "=" in item: 
                        keywd = item.split('=')[0]+'='
                        ret_list.remove(keywd)
                line_list = line.split()
                for i in line_list:
                    if '=' in i:
                        kw = i.split('=')[0]+'='
                        ret_list.remove(kw)
                                    
        else:
            index = line.find('=')
            if index == -1:
                key = line[:begidx].rstrip().replace(' ','_').upper()
                for item in cmddict[key]:
                    if item.startswith(text):
                        ret_list.append(item)
            else:
                left_part = line[:index].split()
                left_part.remove(left_part[-1])
                key = '_'.join(left_part).upper()
                for item in cmddict[key]:
                    if item.startswith(text):
                        ret_list.append(item) 
                line_list = line.split()
                for i in line_list:
                    if '=' in i:
                        kw = i.split('=')[0]+'='
                        ret_list.remove(kw)
        return ret_list

        
    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            import readline
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            a = readline.get_begidx()
            b = readline.get_endidx()
            c = text
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            #####
            # with open('/Users/yangbo/Desktop/log.txt','w+') as f:
            #     f.write(f"buffer:{origline}    ")
            #     f.write(f"get_begidx:{a}   ")
            #     f.write(f"get_endidx:{b}   ")
            #     f.write(f"text:${c}$   ")
            #     f.write(f"stripped:{stripped}   ")
            #     f.write(f"begidx:{begidx}   ")
            #     f.write(f"endidx:{endidx}"+"\n")
            #     f.close()
            #####
            if begidx>0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None


if __name__ == "__main__":
    args = sys.argv
    cli = Cli()
    if len(args) == 1:
        cli.cmdloop()
    else:
        arg = args[1:]
        arg = " ".join(arg)
        cli.onecmd(arg)
    
