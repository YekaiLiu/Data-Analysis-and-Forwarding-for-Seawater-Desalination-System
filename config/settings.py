
times=33
USING_FILE = True
class global_var:
    flag =0                                #����desalination���������ݵĻ�����ʾ
    flag1=''  #qmlviewԭ���ѱ�#ע�ͣ�filename#���ڱ���ѡȡ��pcapng�ļ�·��
    flag2=0   #qmlviewԭ���ѱ�#ע�ͣ�flag   #��filedialog��python.exe����֮����� 
    flag3=0 #���������adam2����ת������̨mysql�������е����ݿ��equipment�б�ADAM2��Ӧ��id��
#���Ҿ����˴���id��������20����
    flag4=0#���������adam1����ת������̨mysql�������е����ݿ��equipment�б�ADAM1��Ӧ��id��
#���Ҿ����˴���id��������20����
    flag5=0   #ADAM3
    flag6=0   #windturb1

def sv(flagvalue):
    global_var.flag = flagvalue
def gv():
    return global_var.flag

def ss(flag1str):
    global_var.flag1 = flag1str
def gs():
    #return global_var.flag1str ��wrong������
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







