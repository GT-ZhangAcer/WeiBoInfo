import sys

def workPath():
    ScriptFilePath=(sys.argv[0])#获得的是当前执行脚本的位置（若在命令行执行的该命令，则为空）
    try:
        WorkPathNum=ScriptFilePath.rindex('/')
    except:
        WorkPathNum = ScriptFilePath.rindex('\\')
    WorkPath=ScriptFilePath[0:WorkPathNum+1]#切片
    print("当前工作目录为："+WorkPath)
    return  WorkPath

def debug_SEcontents_A(HTMLinfo):#各父标签的目录树
    print(len(HTMLinfo[0]))
    for i in range(len(HTMLinfo)):
        print(str(i) + "---\n" + str(HTMLinfo[i].contents))
def debug_SEcontents_B(HTMLinfo):#第一个父标签下的目录树
    print(len(HTMLinfo[0].contents))
    for i in range(len(HTMLinfo[0].contents)):
        print(str(i) + "---\n" + str(HTMLinfo[0].contents[i]))

def debug_SEcontents_C(HTMLinfo):#父标签下的目录树
    print(len(HTMLinfo.contents))
    for i in range(len(HTMLinfo.contents)):
        print(str(i) + "---\n" + str(HTMLinfo.contents[i]))