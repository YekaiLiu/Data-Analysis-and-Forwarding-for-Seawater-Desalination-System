
times=33
USING_FILE = True
class global_var:
    flag =0                                #用于desalination界面中数据的缓速显示
    flag1=''  #qmlview原（已被#注释）filename#用于保存选取的pcapng文件路径
    flag2=0   #qmlview原（已被#注释）flag   #让filedialog在python.exe窗口之后出来 
    flag3=0 #将解析后的adam2数据转发至后台mysql服务器中的数据库表equipment中表ADAM2对应的id中
#并且决定了存入id的条数（20条）
    flag4=0#将解析后的adam1数据转发至后台mysql服务器中的数据库表equipment中表ADAM1对应的id中
#并且决定了存入id的条数（20条）
    flag5=0   #ADAM3
    flag6=0   #windturb1

def sv(flagvalue):
    global_var.flag = flagvalue
def gv():
    return global_var.flag

def ss(flag1str):
    global_var.flag1 = flag1str
def gs():
    #return global_var.flag1str （wrong！！）
    return global_var.flag1

def sv2(flag2value):
    global_var.flag2 = flag2value
def gv2():
    return global_var.flag2

def sv3(flag3value):
    global_var.flag3 = flag3value
def gv3():
    return global_var.flag3

def sv4(flag4value):
    global_var.flag4 = flag4value
def gv4():
    return global_var.flag4

def sv5(flag5value):
    global_var.flag5 = flag5value
def gv5():
    return global_var.flag5

def sv6(flag6value):
    global_var.flag6 = flag6value
def gv6():
    return global_var.flag6







