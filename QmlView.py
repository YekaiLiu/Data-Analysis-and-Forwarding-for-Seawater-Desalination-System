from PyQt5.QtCore import QUrl,  pyqtSlot, pyqtSignal, QThread
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
import random
import tkinter as tk  # 3.2版本后自带的python库 python自带的图形界面库
from tkinter import filedialog  # 3.2版本后自带的python库
import pymysql
import pyshark
import struct

'''
PyMySQL，它是在 Python3.x 版本中用于连接MySQL服务器的一个库，Python2中则使用mysqldb。

本设计软件采用Python3.6编程分析用户所选择的PCAPNG Wireshark数据包文件,根据实际协议解析得到各项有效数据；并利用QML语言结合Qt Quick模块创建图形化
用户界面；再通过PyQt5将QML设计的界面和Python应用程序结合起来，从而使得基于QML设计的图形用户界面能够动态及时地显示在Python脚本中进行的协议解析过程
所得到的各项数据；同时软件程序会通过pymysql模块连接到已启动的MySQL5.7.9后台服务器data_repost中已建立的equipment数据库，并且按实际需求将解析得到
的数据插入该后台服务器数据库的相应表中。

协议解析，界面展示，数据库备份，数据转发后台都完成了！
'''
import config.ip
import config.settings

config.settings.gv()  # 引用全局变量
config.settings.sv(0)  # 修改全局变量

config.settings.gs()
config.settings.ss('')

config.settings.gv2()  # 引用全局变量
config.settings.sv2(0)  # 修改全局变量

config.settings.gv3()# 引用全局变量
config.settings.sv3(1)# 修改全局变量   for ADAM2 transfer use

config.settings.gv4()# 引用全局变量
config.settings.sv4(1)# 修改全局变量   for ADAM1 transfer use


config.settings.gv5()# 引用全局变量
config.settings.sv5(1)# 修改全局变量   for ADAM3 transfer use

config.settings.gv6()# 引用全局变量
config.settings.sv6(1)# 修改全局变量   for windturb1 transfer use


class QmlView(QQuickView):
    def __init__(self):
        super().__init__()
        self.data_source = DataSource()
        self.data_source.sigUpdate.connect(self.update)
        self.data_source.start()

    @pyqtSlot(str, str)
    def update(self, prop, value):
        self.rootObject().setProperty(prop, value)


class DataSource(QThread):
    sigUpdate = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.sniff_data()

    def sniff_data(self):
        if (config.settings.USING_FILE and 0 != config.settings.gv2()):  ##加在这里可以 让filedialog在python.exe窗口之后出来
            root = tk.Tk()  #
            root.withdraw()  # 这样可以把t框给关掉了！很好
            print("请选择需要进行解析的网络数据包")
            print()
            config.settings.ss(filedialog.askopenfilename(filetypes=[("抓包数据文件", "pcapng")]))

        if '' != config.settings.gs():  # 加了这句后就不会因为不选文件或  者点了取消对话框而崩溃了
            correspondingfilename = config.settings.gs().replace('/', '\\')
            cap = pyshark.FileCapture(correspondingfilename)
            printinfo = ''
            printinfo = '对' + config.settings.gs() + '路径下的wireshark数据包文件（pcapng）' \
                                                     '进行协议解析,并将得到的各项有效数据实时动态展示在人机交互界面中，同时按实际需求将解析得到的部分数据转发至MySQL后台服务器的euiqpment数据库中。'
            print(printinfo)
            # 路径下的wireshark数据包文件（pcapng）进行协议解析得到的各项有效数据已展示在人机交互界面中
            for p in cap:
                if 'MODBUS' in p:
                    if p['IP'].src == config.ip.WINDTURB1:
                        self.packet_windturbine_1(p)
                    elif p['IP'].src == config.ip.WINDTURB2:
                        # TODO
                        self.packet_windturbine_2(p)
                    elif p['IP'].src == config.ip.PCS:
                        self.packet_PCS(p)
                    elif p['IP'].src == config.ip.BMS:
                        self.packet_BMS(p)
                    elif p['IP'].src == config.ip.DESALINPLANT:
                        # TODO
                        if 40 == config.settings.gv():
                            config.settings.sv(0)
                            self.packet_desalinplant(p)
                        else:
                            config.settings.sv(config.settings.gv() + 1)
                    elif p['IP'].src == config.ip.ADAM1:
                        self.packet_adam1(p)
                    elif p['IP'].src == config.ip.ADAM2:
                        self.packet_adam2(p)
                    elif p['IP'].src == config.ip.ADAM3:
                        self.packet_adam3(p)
                else:
                    continue
        else:
            return

    def packet_adam3(self, packet):
        packet_data_str = []
        if packet['MODBUS'].func_code == '1':
            pass
        else:
            return
        if packet['MODBUS'].byte_cnt == '2':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if len(packet_data_str) < 12:
                        packet_data_str.append(field.raw_value)
            n = len(packet_data_str)  # 12
            a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12 = packet_data_str[0: n]  # '0c', '00'
            aa = a11 + a12  # 0c00
            aaa = aa[::-1]  # 00c0
            list1 = list(aaa)  # 0 0 c 0
            m = len(list1)
            b1, b2, b3, b4 = list1[0:m]
            if b1 == '0':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 0, 0, 0]
            elif b1 == '1':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 0, 0, 1]
            elif b1 == '2':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 0, 1, 0]
            elif b1 == '3':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 0, 1, 1]
            elif b1 == '4':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 1, 0, 0]
            elif b1 == '5':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 1, 0, 1]
            elif b1 == '6':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 1, 1, 0]
            elif b1 == '7':
                adam3di3, adam3di2, adam3di1, adam3di0 = [0, 1, 1, 1]
            elif b1 == '8':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 0, 0, 0]
            elif b1 == '9':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 0, 0, 1]
            elif b1 == 'a':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 0, 1, 0]
            elif b1 == 'b':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 0, 1, 1]
            elif b1 == 'c':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 1, 0, 0]
            elif b1 == 'd':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 1, 0, 1]
            elif b1 == 'e':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 1, 1, 0]
            elif b1 == 'f':
                adam3di3, adam3di2, adam3di1, adam3di0 = [1, 1, 1, 1]
            if b2 == '0':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 0, 0, 0]
            elif b2 == '1':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 0, 0, 1]
            elif b2 == '2':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 0, 1, 0]
            elif b2 == '3':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 0, 1, 1]
            elif b2 == '4':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 1, 0, 0]
            elif b2 == '5':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 1, 0, 1]
            elif b2 == '6':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 1, 1, 0]
            elif b2 == '7':
                adam3di7, adam3di6, adam3di5, adam3di4 = [0, 1, 1, 1]
            elif b2 == '8':
                adam3di7, adam3di6, adam3di5, adam3di4 = [1, 0, 0, 0]
            elif b2 == '9':
                adam3di7, adam3di6, adam3di5, adam3di4 = [1, 0, 0, 1]
            elif b2 == 'a':
                adam3di7, adam3di6, adam3di5, adam3di4 = [1, 0, 1, 0]
            elif b2 == 'b':
                adam3di7, adam3di6, adam3di5, adam3di4 = [1, 0, 1, 1]
            elif b2 == 'c':
                adam3di7, adam3di6, adam3di5, adam3di4 = [1, 1, 0, 0]
            elif b2 == 'd':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 1, 0, 1]
            elif b2 == 'e':
                adam3di7, adam3di6, adam3di5, adam3di4 = [1, 1, 1, 0]
            elif b2 == 'f':
                adam3di7, adam3di6, adam3di5, adam3di4 = [1, 1, 1, 1]
            if b3 == '0':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 0, 0, 0]
            elif b3 == '1':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 0, 0, 1]
            elif b3 == '2':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 0, 1, 0]
            elif b3 == '3':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 0, 1, 1]
            elif b3 == '4':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 1, 0, 0]
            elif b3 == '5':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 1, 0, 1]
            elif b3 == '6':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 1, 1, 0]
            elif b3 == '7':
                adam3di11, adam3di10, adam3di9, adam3di8 = [0, 1, 1, 1]
            elif b2 == '8':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 0, 0, 0]
            elif b3 == '9':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 0, 0, 1]
            elif b3 == 'a':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 0, 1, 0]
            elif b3 == 'b':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 0, 1, 1]
            elif b3 == 'c':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 1, 0, 0]
            elif b3 == 'd':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 1, 0, 1]
            elif b3 == 'e':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 1, 1, 0]
            elif b3 == 'f':
                adam3di11, adam3di10, adam3di9, adam3di8 = [1, 1, 1, 1]
            if adam3di0 == 1:
                self.setProperty_wrap('adam3di0str', '正常')
            elif adam3di0 == 0:
                self.setProperty_wrap('adam3di0str', '动作')
            if adam3di1 == 1:
                self.setProperty_wrap('adam3di1str', '闭合')
            elif adam3di1 == 0:
                self.setProperty_wrap('adam3di1str', '断开')
            if adam3di2 == 1:
                self.setProperty_wrap('adam3di2str', '闭合')
            elif adam3di2 == 0:
                self.setProperty_wrap('adam3di2str', '断开')
            if adam3di3 == 1:
                self.setProperty_wrap('adam3di3str', '闭合')
            elif adam3di3 == 0:
                self.setProperty_wrap('adam3di3str', '断开')
            if adam3di4 == 1:
                self.setProperty_wrap('adam3di4str', '闭合')
            elif adam3di4 == 0:
                self.setProperty_wrap('adam3di4str', '断开')
            if adam3di5 == 1:
                self.setProperty_wrap('adam3di5str', '正常')
            elif adam3di5 == 0:
                self.setProperty_wrap('adam3di5str', '报警')
            if adam3di6 == 1:
                self.setProperty_wrap('adam3di6str', '正常')
            elif adam3di6 == 0:
                self.setProperty_wrap('adam3di6str', '报警')
            if adam3di7 == 1:
                self.setProperty_wrap('adam3di7str', '闭合')
            elif adam3di7 == 0:
                self.setProperty_wrap('adam3di7str', '断开')

            db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='', db='equipment', charset='utf8')
            cursor = db.cursor()
            sql = "REPLACE INTO ADAM3 (id,浪涌保护状态位adam3di0,220V供电总空开状态位adam3di1,220_24V开关电源状态位adam3di2,\
            24V空开状态位adam3di3,散热_除湿空开状态位adam3di4,控制柜UPS1报警状态位adam3di5,控制柜UPS2报警状态位adam3di6,\
            海淡负载断路器状态位adam3di7) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s','%s','%s')"
            if config.settings.gv5() <= 10:
                #not enough arguments for format string是因为data与values元素数目不一致
                data = (config.settings.gv5(), adam3di0, adam3di1, adam3di2,adam3di3, adam3di4, adam3di5, adam3di6, adam3di7)
                config.settings.sv5(config.settings.gv5() + 1)
                cursor.execute(sql % data)
                db.commit()
            else:
                if config.settings.gv5() == 11:
                    print()
                    print('解析得到的微网系统电控柜硬件表ADAM-6020-3的数据已转发至MySQL后台服务器euiqpment数据库的表ADAM3中！')
                    config.settings.sv5(config.settings.gv5() + 1)
                    return
                else:
                    return

    def packet_adam2(self, packet):
        packet_data_str = []
        # 执行到这里了
        if packet['MODBUS'].func_code == '1':
            pass
        else:
            return
        if packet['MODBUS'].byte_cnt == '2':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        # print(field.main_field.get_default_value(), ' ', field.raw_value)
                        packet_data_str.append(field.raw_value)

                if isinstance(field, pyshark.packet.layer.LayerField):
                    if len(packet_data_str) < 12:
                        packet_data_str.append(field.raw_value)
            n = len(packet_data_str)  # 12
            a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12 = packet_data_str[0: n]  # '0c', '00'
            aa = a11 + a12
            aaa = aa[::-1]
            list1 = list(aaa)
            m = len(list1)
            b1, b2, b3, b4 = list1[0:m]
            if b1 == '0':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 0, 0, 0]
            elif b1 == '1':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 0, 0, 1]
            elif b1 == '2':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 0, 1, 0]
            elif b1 == '3':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 0, 1, 1]
            elif b1 == '4':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 1, 0, 0]
            elif b1 == '5':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 1, 0, 1]
            elif b1 == '6':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 1, 1, 0]
            elif b1 == '7':
                adam2di3, adam2di2, adam2di1, adam2di0 = [0, 1, 1, 1]
            elif b1 == '8':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 0, 0, 0]
            elif b1 == '9':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 0, 0, 1]
            elif b1 == 'a':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 0, 1, 0]
            elif b1 == 'b':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 0, 1, 1]
            elif b1 == 'c':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 1, 0, 0]
            elif b1 == 'd':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 1, 0, 1]
            elif b1 == 'e':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 1, 1, 0]
            elif b1 == 'f':
                adam2di3, adam2di2, adam2di1, adam2di0 = [1, 1, 1, 1]
            if b2 == '0':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 0, 0, 0]
            elif b2 == '1':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 0, 0, 1]
            elif b2 == '2':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 0, 1, 0]
            elif b2 == '3':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 0, 1, 1]
            elif b2 == '4':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 1, 0, 0]
            elif b2 == '5':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 1, 0, 1]
            elif b2 == '6':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 1, 1, 0]
            elif b2 == '7':
                adam2di7, adam2di6, adam2di5, adam2di4 = [0, 1, 1, 1]
            elif b2 == '8':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 0, 0, 0]
            elif b2 == '9':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 0, 0, 1]
            elif b2 == 'a':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 0, 1, 0]
            elif b2 == 'b':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 0, 1, 1]
            elif b2 == 'c':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 1, 0, 0]
            elif b2 == 'd':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 1, 0, 1]
            elif b2 == 'e':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 1, 1, 0]
            elif b2 == 'f':
                adam2di7, adam2di6, adam2di5, adam2di4 = [1, 1, 1, 1]
            if b3 == '0':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 0, 0, 0]
            elif b3 == '1':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 0, 0, 1]
            elif b3 == '2':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 0, 1, 0]
            elif b3 == '3':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 0, 1, 1]
            elif b3 == '4':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 1, 0, 0]
            elif b3 == '5':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 1, 0, 1]
            elif b3 == '6':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 1, 1, 0]
            elif b3 == '7':
                adam2di11, adam2di10, adam2di9, adam2di8 = [0, 1, 1, 1]
            elif b2 == '8':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 0, 0, 0]
            elif b3 == '9':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 0, 0, 1]
            elif b3 == 'a':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 0, 1, 0]
            elif b3 == 'b':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 0, 1, 1]
            elif b3 == 'c':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 1, 0, 0]
            elif b3 == 'd':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 1, 0, 1]
            elif b3 == 'e':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 1, 1, 0]
            elif b3 == 'f':
                adam2di11, adam2di10, adam2di9, adam2di8 = [1, 1, 1, 1]
            if adam2di0 == 1:
                self.setProperty_wrap('adam2di0str', '闭合')
            elif adam2di0 == 0:
                self.setProperty_wrap('adam2di0str', '断开')
            if adam2di2 == 1:
                self.setProperty_wrap('adam2di2str', '正常')
            elif adam2di2 == 0:
                self.setProperty_wrap('adam2di2str', '跳开')
            if adam2di4 == 1:
                self.setProperty_wrap('adam2di4str', '正常')
            elif adam2di4 == 0:
                self.setProperty_wrap('adam2di4str', '跳开')
            if adam2di6 == 1:
                self.setProperty_wrap('adam2di6str', '吸合')
            elif adam2di6 == 0:
                self.setProperty_wrap('adam2di6str', '分开')
            if adam2di8 == 1:
                self.setProperty_wrap('adam2di8str', '吸合')
            elif adam2di8 == 0:
                self.setProperty_wrap('adam2di8str', '分开')
            if adam2di10 == 1:
                self.setProperty_wrap('adam2di10str', '闭合')
            elif adam2di10 == 0:
                self.setProperty_wrap('adam2di10str', '断开')
            db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='', db='equipment', charset='utf8')
            cursor = db.cursor()
            sql = "REPLACE INTO ADAM2 (id,照明断路器状态位adam2di0,空调热继状态位adam2di2,照明热继状态位adam2di4,\
            空调接触器状态位adam2di6,照明接触器状态位adam2di8,滤波器断路器状态位adam2di10) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s')"
            '''
            REPLACE的运行与INSERT很相像,但是如果旧记录与新记录有相同的值，则在新记录被插入之前，旧记录被删除，即：

            1.    尝试把新行插入到表中 

            2.    当因为对于主键或唯一关键字出现重复关键字错误而造成插入失败时：

                    从表中删除含有重复关键字值的冲突行

                    再次尝试把新行插入到表中
            '''
            if config.settings.gv3() <= 10:
                data = (config.settings.gv3(), adam2di0, adam2di2, adam2di4, adam2di6, adam2di8, adam2di10)
                config.settings.sv3(config.settings.gv3() + 1)
                cursor.execute(sql % data)
                db.commit()
            else:
                if config.settings.gv3() == 11:
                    print()
                    print('解析得到的微网系统电控柜硬件表ADAM-6020-2的数据已转发至MySQL后台服务器euiqpment数据库的表ADAM2中！')
                    config.settings.sv3(config.settings.gv3() + 1)
                else:
                    return

    def packet_adam1(self, packet):
        packet_data_str = []
        # 执行到这里了
        if packet['MODBUS'].func_code == '1':
            pass
        else:
            return
        if packet['MODBUS'].byte_cnt == '2':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if len(packet_data_str) < 12:
                        packet_data_str.append(field.raw_value)
            n = len(packet_data_str)  # 12
            a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12 = packet_data_str[0: n]  # '0c', '3c'
            aa = a11 + a12  # 0c3c
            aaa = aa[::-1]  # c3c0
            list1 = list(aaa)  # c 3 c 0
            m = len(list1)
            b1, b2, b3, b4 = list1[0:m]  # b1=c  b2=3  b3=c  b4=0
            if b1 == '0':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 0, 0, 0]
            elif b1 == '1':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 0, 0, 1]
            elif b1 == '2':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 0, 1, 0]
            elif b1 == '3':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 0, 1, 1]
            elif b1 == '4':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 1, 0, 0]
            elif b1 == '5':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 1, 0, 1]
            elif b1 == '6':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 1, 1, 0]
            elif b1 == '7':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 1, 1, 1]
            elif b1 == '8':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 0, 0, 0]
            elif b1 == '9':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 0, 0, 1]
            elif b1 == 'a':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 0, 1, 0]
            elif b1 == 'b':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 0, 1, 1]
            elif b1 == 'c':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 1, 0, 0]
            elif b1 == 'd':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 1, 0, 1]
            elif b1 == 'e':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 1, 1, 0]
            elif b1 == 'f':
                adam1di3, adam1di2, adam1di1, adam1di0 = [1, 1, 1, 1]
            if b2 == '0':
                adam1di7, adam1di6, adam1di5, adam1di4 = [0, 0, 0, 0]
            elif b2 == '1':
                adam1di7, adam1di6, adam1di5, adam1di4 = [0, 0, 0, 1]
            elif b2 == '2':
                adam1di7, adam1di6, adam1di5, adam1di4 = [0, 0, 1, 0]
            elif b2 == '3':
                adam1di7, adam1di6, adam1di5, adam1di4 = [0, 0, 1, 1]
            elif b2 == '4':
                adam1di7, adam1di6, adam1di5, adam1di4 = [0, 1, 0, 0]
            elif b2 == '5':
                adam1di3, adam1di2, adam1di1, adam1di0 = [0, 1, 0, 1]
            elif b2 == '6':
                adam1di7, adam1di6, adam1di5, adam1di4 = [0, 1, 1, 0]
            elif b2 == '7':
                adam1di7, adam1di6, adam1di5, adam1di4 = [0, 1, 1, 1]
            elif b2 == '8':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 0, 0, 0]
            elif b2 == '9':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 0, 0, 1]
            elif b2 == 'a':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 0, 1, 0]
            elif b2 == 'b':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 0, 1, 1]
            elif b2 == 'c':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 1, 0, 0]
            elif b2 == 'd':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 1, 0, 1]
            elif b2 == 'e':
                aadam1di7, adam1di6, adam1di5, adam1di4 = [1, 1, 1, 0]
            elif b2 == 'f':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 1, 1, 1]
            if b3 == '0':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 0, 0, 0]
            elif b3 == '1':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 0, 0, 1]
            elif b3 == '2':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 0, 1, 0]
            elif b3 == '3':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 0, 1, 1]
            elif b3 == '4':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 1, 0, 0]
            elif b3 == '5':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 1, 0, 1]
            elif b3 == '6':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 1, 1, 0]
            elif b3 == '7':
                adam1di11, adam1di10, adam1di9, adam1di8 = [0, 1, 1, 1]
            elif b2 == '8':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 0, 0, 0]
            elif b3 == '9':
                adam1di7, adam1di6, adam1di5, adam1di4 = [1, 0, 0, 1]
            elif b3 == 'a':
                adam1di11, adam1di10, adam1di9, adam1di8 = [1, 0, 1, 0]
            elif b3 == 'b':
                adam1di11, adam1di10, adam1di9, adam1di8 = [1, 0, 1, 1]
            elif b3 == 'c':
                adam1di11, adam1di10, adam1di9, adam1di8 = [1, 1, 0, 0]
            elif b3 == 'd':
                adam1di11, adam1di10, adam1di9, adam1di8 = [1, 1, 0, 1]
            elif b3 == 'e':
                adam1di11, adam1di10, adam1di9, adam1di8 = [1, 1, 1, 0]
            elif b3 == 'f':
                adam1di11, adam1di10, adam1di9, adam1di8 = [1, 1, 1, 1]
            if adam1di1 == 1:
                self.setProperty_wrap('adam1di1str', '闭合')
            elif adam1di1 == 0:
                self.setProperty_wrap('adam1di1str', '断开')
            if adam1di0 == 1:
                self.setProperty_wrap('adam1di0str', '闭合')
            elif adam1di0 == 0:
                self.setProperty_wrap('adam1di0str', '断开')
            if adam1di2 == 1:
                self.setProperty_wrap('adam1di2str', '闭合')
            elif adam1di2 == 0:
                self.setProperty_wrap('adam1di2str', '断开')
            if adam1di4 == 1:
                self.setProperty_wrap('adam1di4str', '闭合')
            elif adam1di4 == 0:
                self.setProperty_wrap('adam1di4str', '断开')
            if adam1di5 == 1:
                self.setProperty_wrap('adam1di5str', '闭合')
            elif adam1di5 == 0:
                self.setProperty_wrap('adam1di5str', '断开')
            if adam1di6 == 1:
                self.setProperty_wrap('adam1di6str', '正常')
            elif adam1di6 == 0:
                self.setProperty_wrap('adam1di6str', '故障')
            if adam1di7 == 1:
                self.setProperty_wrap('adam1di7str', '正常')
            elif adam1di7 == 0:
                self.setProperty_wrap('adam1di7str', '报警')
            if adam1di8 == 1:
                self.setProperty_wrap('adam1di8str', '闭合')
            elif adam1di8 == 0:
                self.setProperty_wrap('adam1di8str', '断开')
            if adam1di9 == 1:
                self.setProperty_wrap('adam1di9str', '闭合')
            elif adam1di9 == 0:
                self.setProperty_wrap('adam1di9str', '断开')
            if adam1di10 == 1:
                self.setProperty_wrap('adam1di10str', '闭合')
            elif adam1di10 == 0:
                self.setProperty_wrap('adam1di10str', '断开')
            db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='', db='equipment', charset='utf8')
            cursor = db.cursor()
            sql = "REPLACE INTO ADAM1 (id,柴发断路器状态位adam1di0,风机1断路器状态位adam1di1,\
            风机2断路器状态位adam1di2,PCS断路器状态位adam1di4,电气柜UPS断路器状态位adam1di5, 电气柜UPS故障状态位adam1di6, \
            电气柜UPS报警状态位adam1di7,居民断路器状态位adam1di8, 空调断路器状态位adam1di10) \
            VALUES( % d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            if config.settings.gv4() <= 10:
                data = (
                config.settings.gv4(), adam1di0, adam1di1, adam1di2, adam1di4, adam1di5, adam1di6, adam1di7, adam1di8,\
                adam1di10)
                # config.settings.sv4(config.settings.gv4() + 1)
                cursor.execute(sql % data)
                db.commit()
            else:
                return
        elif packet['MODBUS'].byte_cnt == '1':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if len(packet_data_str) < 1:
                        packet_data_str.append(field.raw_value)
            c = ','.join(packet_data_str)
            cc = c[::-1]
            list2 = list(cc)  #
            b1, b2 = list2[0:2]
            if b1 == '0':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 0, 0, 0]
            elif b1 == '1':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 0, 0, 1]
            elif b1 == '2':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 0, 1, 0]
            elif b1 == '3':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 0, 1, 1]
            elif b1 == '4':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 1, 0, 0]
            elif b1 == '5':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 1, 0, 1]
            elif b1 == '6':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 1, 1, 0]
            elif b1 == '7':
                adam1do3, adam1do2, adam1do1, adam1do0 = [0, 1, 1, 1]
            elif b1 == '8':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 0, 0, 0]
            elif b1 == '9':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 0, 0, 1]
            elif b1 == 'a':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 0, 1, 0]
            elif b1 == 'b':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 0, 1, 1]
            elif b1 == 'c':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 1, 0, 0]
            elif b1 == 'd':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 1, 0, 1]
            elif b1 == 'e':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 1, 1, 0]
            elif b1 == 'f':
                adam1do3, adam1do2, adam1do1, adam1do0 = [1, 1, 1, 1]
            if b2 == '0':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 0, 0, 0]
            elif b2 == '1':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 0, 0, 1]
            elif b2 == '2':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 0, 1, 0]
            elif b2 == '3':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 0, 1, 1]
            elif b2 == '4':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 1, 0, 0]
            elif b2 == '5':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 1, 0, 1]
            elif b2 == '6':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 1, 1, 0]
            elif b2 == '7':
                adam1do7, adam1do6, adam1do5, adam1do4 = [0, 1, 1, 1]
            elif b2 == '8':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 0, 0, 0]
            elif b2 == '9':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 0, 0, 1]
            elif b2 == 'a':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 0, 1, 0]
            elif b2 == 'b':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 0, 1, 1]
            elif b2 == 'c':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 1, 0, 0]
            elif b2 == 'd':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 1, 0, 1]
            elif b2 == 'e':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 1, 1, 0]
            elif b2 == 'f':
                adam1do7, adam1do6, adam1do5, adam1do4 = [1, 1, 1, 1]
            if adam1do0 == 1:
                self.setProperty_wrap('adam1do0str', '得电 ')
            elif adam1do0 == 0:
                self.setProperty_wrap('adam1do0str', '失电')
            if adam1do1 == 1:
                self.setProperty_wrap('adam1do1str', '得电 ')
            elif adam1do1 == 0:
                self.setProperty_wrap('adam1do1str', '失电')
            if adam1do3 == 1:
                self.setProperty_wrap('adam1do3str', '得电 ')
            elif adam1do3 == 0:
                self.setProperty_wrap('adam1do3str', '失电')
            if adam1do5 == 1:
                self.setProperty_wrap('adam1do5str', '得电 ')
            elif adam1do5 == 0:
                self.setProperty_wrap('adam1do5str', '失电')
            db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='',
                                 db='equipment', charset='utf8')
            cursor = db.cursor()
            if config.settings.gv4() <= 10:
               sql = "UPDATE ADAM1 SET 柴发中间继电器状态位adam1do0 = (%s) , 居民中间继电器状态位adam1do1 = (%s),\
               空调中间继电器状态位adam1do3= (%s),照明中间继电器状态位adam1do5= (%s)WHERE id=(%s)"  # id=(%d) wrong!
               cursor.execute(sql, (adam1do0,adam1do1,adam1do3,adam1do5 ,config.settings.gv4()))
               config.settings.sv4(config.settings.gv4() + 1)
               db.commit()
            else:
               if config.settings.gv4() == 11:
                  print()
                  print('解析得到的微网系统电控柜硬件表ADAM-6020-1的数据已转发至MySQL后台服务器euiqpment数据库的表ADAM1中！')
                  config.settings.sv4(config.settings.gv4() + 1)
                  return
               else:
                    return


    def packet_windturbine_1(self, packet):
        packet_data_str = []
        if packet['MODBUS'].func_code == '3':
            pass
        else:
            return
        if packet['MODBUS'].byte_cnt == '24':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
            wtb_1_control_method = struct.unpack('>H', bytes.fromhex(packet_data_str[0]))[0]
            wtb_1_running_mode = struct.unpack('>H', bytes.fromhex(packet_data_str[1]))[0]
            wtb_1_running_state = struct.unpack('>H', bytes.fromhex(packet_data_str[2]))[0]
            wtb_1_message_warn0 = struct.unpack('>H', bytes.fromhex(packet_data_str[3]))[0]
            wtb_1_wind_velo1s = struct.unpack('>h', bytes.fromhex(packet_data_str[4]))[0] / 100.0
            wtb_1_wind_velo5min = struct.unpack('>h', bytes.fromhex(packet_data_str[5]))[0] / 100.0
            wtb_1_wind_dir10min = struct.unpack('>h', bytes.fromhex(packet_data_str[6]))[0] / 10.0
            wtb_1_gen_rot = struct.unpack('>h', bytes.fromhex(packet_data_str[7]))[0] / 100.0
            wtb_1_vane_ang = struct.unpack('>h', bytes.fromhex(packet_data_str[8]))[0] / 10.0
            wtb_1_message_warn1 = struct.unpack('>H', bytes.fromhex(packet_data_str[9]))[0]
            wtb_1_res_0 = packet_data_str[10]
            wtb_1_res_1 = packet_data_str[11]
            self.setProperty_wrap('windturb1_40005', str(wtb_1_wind_velo1s))
            self.setProperty_wrap('windturb1_40006', str(wtb_1_wind_velo5min))
            self.setProperty_wrap('windturb1_40007', str(wtb_1_wind_dir10min))
            self.setProperty_wrap('windturb1_40008', str(wtb_1_gen_rot))
            self.setProperty_wrap('windturb1_40009', str(wtb_1_vane_ang))
            self.split_8b_property(wtb_1_message_warn1, ['windturb1_40010_0', \
                                                         'windturb1_40010_1', \
                                                         'windturb1_40010_2', \
                                                         'windturb1_40010_3', \
                                                         'windturb1_40010_4', \
                                                         'windturb1_40010_5', \
                                                         'windturb1_40010_6', \
                                                         'windturb1_40010_7'])
            self.set_distinct_property(wtb_1_control_method, ['windturb1_40001_1', \
                                                              'windturb1_40001_2'])
            self.set_distinct_property(wtb_1_running_mode, ['windturb1_40002_1', \
                                                            'windturb1_40002_2', \
                                                            'windturb1_40002_3', \
                                                            'windturb1_40002_4'])
            self.set_distinct_property(wtb_1_running_state, ['windturb1_40003_1', \
                                                             'windturb1_40003_2', \
                                                             'windturb1_40003_3', \
                                                             'windturb1_40003_4', \
                                                             'windturb1_40003_5', \
                                                             'windturb1_40003_6'])
            self.set_distinct_property(wtb_1_message_warn0, ['windturb1_40004_1', \
                                                             'windturb1_40004_2', \
                                                             'windturb1_40004_3'])

            if config.settings.gv6() <= config.settings.times:
                dbw11 = pymysql.Connect(host='localhost', port=3306, user='root', passwd='', db='equipment', charset='utf8')
                cursorw11 = dbw11.cursor()   #不能有\ （）出现在id后的名字里！

                sqlw11 = "REPLACE INTO windturb1 (id,机组控制方式状态字_1本地2远程,机组运行模式状态字_1手动2自动3维护4停机,\
                                   机组运行状态状态字_1启动2运行3暂停4停机5急停6空转,报警信息状态字_1正常2警告3故障,风向_度,1s风速_米每秒,\
                                    5min平均风速_米每秒,转速_转每分钟, 桨矩角_度,报警信息1状态字_十进制数值)\
                                    VALUES( % d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')"

                data = ( config.settings.gv6(),wtb_1_control_method, wtb_1_running_mode,wtb_1_running_state, wtb_1_message_warn0,
                        wtb_1_wind_dir10min, wtb_1_wind_velo1s, wtb_1_wind_velo5min, wtb_1_gen_rot, wtb_1_vane_ang, wtb_1_message_warn1)

                cursorw11.execute(sqlw11%data)
                dbw11.commit()      #注意不能都命名为sql要有区分比如sql1,2,3
            

            else:
                return



        elif packet['MODBUS'].byte_cnt == '22':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                         packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if field.get_default_value()[0] == 'R':
                         packet_data_str.append(field.raw_value)
            wtb_1_voltageU = struct.unpack('>h', bytes.fromhex(packet_data_str[0]))[0] / 10.0
            wtb_1_voltageV = struct.unpack('>h', bytes.fromhex(packet_data_str[1]))[0] / 10.0
            wtb_1_voltageW = struct.unpack('>h', bytes.fromhex(packet_data_str[2]))[0] / 10.0
            wtb_1_currentU = struct.unpack('>h', bytes.fromhex(packet_data_str[3]))[0] / 100.0
            wtb_1_currentV = struct.unpack('>h', bytes.fromhex(packet_data_str[4]))[0] / 100.0
            wtb_1_currentW = struct.unpack('>h', bytes.fromhex(packet_data_str[5]))[0] / 100.0
            wtb_1_actpow = struct.unpack('>h', bytes.fromhex(packet_data_str[6]))[0] / 10.0
            wtb_1_reactpow = struct.unpack('>h', bytes.fromhex(packet_data_str[7]))[0] / 10.0
            wtb_1_powfactor = struct.unpack('>h', bytes.fromhex(packet_data_str[8]))[0] / 10000.0
            wtb_1_elec_gened = struct.unpack('>H', bytes.fromhex(packet_data_str[10]))[0] / 100.0 \
                                   + struct.unpack('>H', bytes.fromhex(packet_data_str[9]))[0] / 100.0 * (0x10000)
            self.setProperty_wrap('windturb1_40065', str(wtb_1_voltageU))
            self.setProperty_wrap('windturb1_40066', str(wtb_1_voltageV))
            self.setProperty_wrap('windturb1_40067', str(wtb_1_voltageW))
            self.setProperty_wrap('windturb1_40068', str(wtb_1_currentU))
            self.setProperty_wrap('windturb1_40069', str(wtb_1_currentV))
            self.setProperty_wrap('windturb1_40070', str(wtb_1_currentW))
            self.setProperty_wrap('windturb1_40071', str(wtb_1_actpow))
            self.setProperty_wrap('windturb1_40072', str(wtb_1_reactpow))
            self.setProperty_wrap('windturb1_40073', str(wtb_1_powfactor))
            self.setProperty_wrap('windturb1_40075', str(wtb_1_elec_gened))

            if config.settings.gv6() <= config.settings.times:
                    dbw13 = pymysql.Connect(host='localhost', port=3306, user='root', passwd='',
                                            db='equipment', charset='utf8')
                    cursorw13 = dbw13.cursor()
                    sqlw13 = "UPDATE windturb1 SET 有功功率_kw= (%s),无功功率_kVar=(%s),\
                    累计发电量_kwh=(%s), 电网电压U_V=(%s),电网电压V_V=(%s),电网电压W_V=(%s),输出电流U_A=(%s),输出电流V_A=(%s),输出电流W_A=(%s),功率因数 =(%s)\
                    WHERE id=(%s)"
                    cursorw13.execute(sqlw13, (\
                    wtb_1_actpow, wtb_1_reactpow, wtb_1_elec_gened, wtb_1_voltageU, wtb_1_voltageV, wtb_1_voltageW, \
                    wtb_1_currentU, wtb_1_currentV, wtb_1_currentW, wtb_1_powfactor, config.settings.gv6()))
                    dbw13.commit()
        elif packet['MODBUS'].byte_cnt == '10':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                    if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                       if field.main_field.get_default_value()[0] == 'R':
                          packet_data_str.append(field.raw_value)
                    if isinstance(field, pyshark.packet.layer.LayerField):
                       if field.get_default_value()[0] == 'R':
                          packet_data_str.append(field.raw_value)
            wtb_1_powset = struct.unpack('>H', bytes.fromhex(packet_data_str[3]))[0]
            self.setProperty_wrap('windturb1_40260', str(wtb_1_powset))
            wtb_1_communication_test = struct.unpack('>H', bytes.fromhex(packet_data_str[4]))[0]
            self.setProperty_wrap('windturb1_40261', str(wtb_1_communication_test))
            self.setProperty_wrap('windturb1txgz', '否')
            if config.settings.gv6() <= config.settings.times:
                    dbw12 = pymysql.Connect(host='localhost', port=3306, user='root', passwd='',
                    db='equipment', charset='utf8')
                    cursorw12 = dbw12.cursor()
                    sqlw12 = "UPDATE windturb1 SET 有功给定_kw= (%s),通讯循环检测字_0和1间隔循环代表通讯正常= (%s)WHERE id=(%s)"  # id=(%d) wrong!
                    cursorw12.execute(sqlw12, (wtb_1_powset, wtb_1_communication_test, config.settings.gv6()))
                    dbw12.commit()
                    config.settings.sv6(config.settings.gv6() + 1)
            else:
                      if config.settings.gv6() == config.settings.times+1:
                          print()
                          print('解析得到的风电机组1的数据已转发至MySQL后台服务器euiqpment数据库的表windturb1中！')
                          config.settings.sv6(config.settings.gv6() + 1)
                          return
                      else:
                          return


    def packet_windturbine_2(self, packet):
        packet_data_str = []
        if packet['MODBUS'].func_code == '3':
            pass
        else:
            return
        if packet['MODBUS'].byte_cnt == '26':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
            Add0000 = struct.unpack('>h', bytes.fromhex(packet_data_str[1]))[0] / 10.0  # 风速风向的顺序在协议和界面中调反了
            Add0001 = struct.unpack('>h', bytes.fromhex(packet_data_str[0]))[0] / 10.0
            Add0002 = struct.unpack('>h', bytes.fromhex(packet_data_str[2]))[0] / 10.0
            Add0003 = struct.unpack('>h', bytes.fromhex(packet_data_str[3]))[0] / 10.0
            Add0004 = struct.unpack('>h', bytes.fromhex(packet_data_str[4]))[0] / 10.0
            Add0005 = struct.unpack('>H', bytes.fromhex(packet_data_str[5]))[0]
            Add0006 = struct.unpack('>H', bytes.fromhex(packet_data_str[6]))[0] / 1000.0
            # 协议中的单位是w，但界面中是kw所以显示前要除以1000  还有python中#才可以 //没用的！
            Add0007 = struct.unpack('>h', bytes.fromhex(packet_data_str[7]))[0] / 100.0
            Add0008 = struct.unpack('>H', bytes.fromhex(packet_data_str[8]))[0] / 10.0
            Add0009 = struct.unpack('>H', bytes.fromhex(packet_data_str[9]))[0] / 10.0
            Add0008plus9 = Add0008 + Add0009 * (0x10000)
            A4X0032 = struct.unpack('>H', bytes.fromhex(packet_data_str[10]))[0]
            A4X0033 = struct.unpack('>H', bytes.fromhex(packet_data_str[11]))[0]
            self.split_8b_property(A4X0032, ['w2_4X0032bit0sdzt', \
                                             'w2_4X0032bit1zdzt', \
                                             'w2_4X0032bit2djzt', \
                                             'w2_4X0032bit3yxzt', \
                                             'w2_4X0032bit4tjzt', \
                                             'w2_4X0032bit5jdzt', \
                                             'w2_4X0032bit6yczt', \
                                             'w2_4X0032bit7vain'])

            self.split_8b_property(A4X0033, ['w2_4X0033bit0djcs', \
                                             'w2_4X0033bit1dfbj', \
                                             'w2_4X0033bit2djgz', \
                                             'w2_4X0033bit3nbqgz', \
                                             'w2_4X0033bit4phgz', \
                                             'w2_4X0033bit5bjgz', \
                                             'w2_4X0033bit6ywgz', \
                                             'w2_4X0033bit7txgz'])
            self.setProperty_wrap('windturb2Add0000', str(Add0000))
            self.setProperty_wrap('windturb2Add0001', str(Add0001))
            self.setProperty_wrap('windturb2Add0002', str(Add0002))
            self.setProperty_wrap('windturb2Add0003', str(Add0003))
            self.setProperty_wrap('windturb2Add0004', str(Add0004))
            self.setProperty_wrap('windturb2Add0005', str(Add0005))
            self.setProperty_wrap('windturb2Add0006', str(Add0006))
            self.setProperty_wrap('windturb2Add0007', str(Add0007))
            self.setProperty_wrap('windturb2Add0008plus9', str(Add0008plus9))

    def packet_PCS(self, packet):
        packet_data_str = []
        if packet['MODBUS'].func_code == '3':
            pass
        else:
            return
        if packet['MODBUS'].byte_cnt == '8':
            # NOT USED
            pass

        elif packet['MODBUS'].byte_cnt == '32':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
            pcs_voltageA = struct.unpack('>H', bytes.fromhex(packet_data_str[0]))[0] / 10.0
            pcs_voltageB = struct.unpack('>H', bytes.fromhex(packet_data_str[1]))[0] / 10.0
            pcs_voltageC = struct.unpack('>H', bytes.fromhex(packet_data_str[2]))[0] / 10.0
            pcs_currentA = struct.unpack('>h', bytes.fromhex(packet_data_str[3]))[0] / 10.0
            pcs_currentB = struct.unpack('>h', bytes.fromhex(packet_data_str[4]))[0] / 10.0
            pcs_currentC = struct.unpack('>h', bytes.fromhex(packet_data_str[5]))[0] / 10.0
            pcs_elecfeq = struct.unpack('>H', bytes.fromhex(packet_data_str[6]))[0] / 10.0
            pcs_actpow = struct.unpack('>h', bytes.fromhex(packet_data_str[7]))[0] / 10.0
            pcs_reactpow = struct.unpack('>h', bytes.fromhex(packet_data_str[8]))[0] / 10.0
            pcs_dcvol = struct.unpack('>h', bytes.fromhex(packet_data_str[9]))[0] / 10.0
            pcs_dccur = struct.unpack('>h', bytes.fromhex(packet_data_str[10]))[0] / 10.0
            pcs_dcpow = struct.unpack('>h', bytes.fromhex(packet_data_str[11]))[0] / 10.0
            pcs_sysstate_1 = struct.unpack('>H', bytes.fromhex(packet_data_str[12]))[0]
            # 0x（16进制）13c1的十进制数据即为5057
            pcs_sysstate_2 = struct.unpack('>H', bytes.fromhex(packet_data_str[13]))[0]  # RESERVED
            pcs_sysfaultstate_1 = struct.unpack('>H', bytes.fromhex(packet_data_str[14]))[0]
            pcs_sysfaultstate_2 = struct.unpack('>H', bytes.fromhex(packet_data_str[15]))[0]
            self.setProperty_wrap('pcsAdd2000', str(pcs_voltageA))
            self.setProperty_wrap('pcsAdd2001', str(pcs_voltageB))
            self.setProperty_wrap('pcsAdd2002', str(pcs_voltageC))
            self.setProperty_wrap('pcsAdd2003', str(pcs_currentA))
            self.setProperty_wrap('pcsAdd2004', str(pcs_currentB))
            self.setProperty_wrap('pcsAdd2005', str(pcs_currentC))
            self.setProperty_wrap('pcsAdd2006', str(pcs_elecfeq))
            self.setProperty_wrap('pcsAdd2007', str(pcs_actpow))
            self.setProperty_wrap('pcsAdd2008', str(pcs_reactpow))
            self.setProperty_wrap('pcsAdd2009', str(pcs_dcvol))
            self.setProperty_wrap('pcsAdd2010', str(pcs_dccur))
            self.setProperty_wrap('pcsAdd2011', str(pcs_dcpow))
            self.set_distinct_property_inc0(calc_comb_bit(pcs_sysstate_1, 12, 14), \
                                            ['pcsAdd2012Bit12Val0', \
                                             'pcsAdd2012Bit12Val1', \
                                             'pcsAdd2012Bit12Val2', \
                                             'pcsAdd2012Bit12Val3', \
                                             'pcsAdd2012Bit12Val4', \
                                             'pcsAdd2012Bit12Val5'])
            self.set_distinct_property_inc0(calc_comb_bit(pcs_sysstate_1, 4, 5), \
                                            ['pcsAdd2012Bit4Val0', \
                                             '', \
                                             'pcsAdd2012Bit4Val2'])
            self.set_distinct_property_inc0(calc_comb_bit(pcs_sysstate_1, 0, 1), \
                                            ['pcsAdd2012Bit0Val0', \
                                             'pcsAdd2012Bit0Val1', \
                                             'pcsAdd2012Bit0Val2'])
            self.split_16b_property(pcs_sysfaultstate_1, ['pcsAdd2014Bit0', \
                                                          'pcsAdd2014Bit1', \
                                                          'pcsAdd2014Bit2', \
                                                          'pcsAdd2014Bit3', \
                                                          'pcsAdd2014Bit4', \
                                                          'pcsAdd2014Bit5', \
                                                          'pcsAdd2014Bit6', \
                                                          'pcsAdd2014Bit7', \
                                                          'pcsAdd2014Bit8', \
                                                          'pcsAdd2014Bit9', \
                                                          'pcsAdd2014Bit10', \
                                                          'pcsAdd2014Bit11', \
                                                          'pcsAdd2014Bit12', \
                                                          'pcsAdd2014Bit13', \
                                                          'pcsAdd2014Bit14', \
                                                          'pcsAdd2014Bit15'])
            self.split_nb_property(pcs_sysfaultstate_2, ['pcsAdd2015Bit0'], 1)

    def packet_BMS(self, packet):
        packet_data_str = []
        if packet['MODBUS'].func_code == '3':
            pass
        else:
            return
        if packet['MODBUS'].byte_cnt == '62':
            for field in packet['MODBUS']._get_all_fields_with_alternates():
                if isinstance(field, pyshark.packet.layer.LayerFieldsContainer):
                    if field.main_field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
                if isinstance(field, pyshark.packet.layer.LayerField):
                    if field.get_default_value()[0] == 'R':
                        packet_data_str.append(field.raw_value)
            bms_state = struct.unpack('>H', bytes.fromhex(packet_data_str[0]))[0]
            bms_warning = struct.unpack('>H', bytes.fromhex(packet_data_str[1]))[0]
            bms_reserved0 = struct.unpack('>H', bytes.fromhex(packet_data_str[2]))[0]
            bms_voltage_1 = struct.unpack('>H', bytes.fromhex(packet_data_str[3]))[0] / 10.0
            bms_voltage_2 = struct.unpack('>H', bytes.fromhex(packet_data_str[4]))[0] / 10.0
            bms_voltage = struct.unpack('>H', bytes.fromhex(packet_data_str[5]))[0] / 10.0
            bms_current_1 = struct.unpack('>h', bytes.fromhex(packet_data_str[6]))[0] / 10.0
            bms_current_2 = struct.unpack('>h', bytes.fromhex(packet_data_str[7]))[0] / 10.0
            bms_current = struct.unpack('>h', bytes.fromhex(packet_data_str[8]))[0] / 10.0
            bms_soc_1 = struct.unpack('>H', bytes.fromhex(packet_data_str[9]))[0] / 100.0
            bms_soc_2 = struct.unpack('>H', bytes.fromhex(packet_data_str[10]))[0] / 100.0
            bms_soc = struct.unpack('>H', bytes.fromhex(packet_data_str[11]))[0] / 100.0
            bms_soh_1 = struct.unpack('>H', bytes.fromhex(packet_data_str[12]))[0] / 100.0
            bms_soh_2 = struct.unpack('>H', bytes.fromhex(packet_data_str[13]))[0] / 100.0
            bms_soh = struct.unpack('>H', bytes.fromhex(packet_data_str[14]))[0] / 100.0
            bms_tocharge_1 = struct.unpack('>H', bytes.fromhex(packet_data_str[15]))[0]
            bms_tocharge_2 = struct.unpack('>H', bytes.fromhex(packet_data_str[16]))[0]
            bms_tocharge = struct.unpack('>H', bytes.fromhex(packet_data_str[17]))[0]
            bms_remain_1 = struct.unpack('>H', bytes.fromhex(packet_data_str[18]))[0]
            bms_remain_2 = struct.unpack('>H', bytes.fromhex(packet_data_str[19]))[0]
            bms_remain = struct.unpack('>H', bytes.fromhex(packet_data_str[20]))[0]
            bms_highvol_id = struct.unpack('>H', bytes.fromhex(packet_data_str[21]))[0]
            bms_highvol_vol = struct.unpack('>H', bytes.fromhex(packet_data_str[22]))[0] / 1000.0  # /10000.0
            bms_lowvol_id = struct.unpack('>H', bytes.fromhex(packet_data_str[23]))[0]
            bms_lowvol_vol = struct.unpack('>H', bytes.fromhex(packet_data_str[24]))[0] / 1000.0  # /10000.0
            bms_hightem_id = struct.unpack('>H', bytes.fromhex(packet_data_str[25]))[0]
            bms_hightem_tem = struct.unpack('>h', bytes.fromhex(packet_data_str[26]))[0]  # /100.0
            bms_lowtem_id = struct.unpack('>H', bytes.fromhex(packet_data_str[27]))[0]
            bms_lowtem_tem = struct.unpack('>h', bytes.fromhex(packet_data_str[28]))[0]  # /100.0
            self.setProperty_wrap('bmsAdd0004', str(bms_voltage_1))
            self.setProperty_wrap('bmsAdd0005', str(bms_voltage_2))
            self.setProperty_wrap('bmsAdd0006', str(bms_voltage))
            self.setProperty_wrap('bmsAdd0007', str(bms_current_1))
            self.setProperty_wrap('bmsAdd0008', str(bms_current_2))
            self.setProperty_wrap('bmsAdd0009', str(bms_current))
            self.setProperty_wrap('bmsAdd0010', str(bms_soc_1))
            self.setProperty_wrap('bmsAdd0011', str(bms_soc_2))
            self.setProperty_wrap('bmsAdd0012', str(bms_soc))
            self.setProperty_wrap('bmsAdd0013', str(bms_soh_1))
            self.setProperty_wrap('bmsAdd0014', str(bms_soh_2))
            self.setProperty_wrap('bmsAdd0015', str(bms_soh))
            self.setProperty_wrap('bmsAdd0016', str(bms_tocharge_1))
            self.setProperty_wrap('bmsAdd0017', str(bms_tocharge_2))
            self.setProperty_wrap('bmsAdd0018', str(bms_tocharge))
            self.setProperty_wrap('bmsAdd0019', str(bms_remain_1))
            self.setProperty_wrap('bmsAdd0020', str(bms_remain_2))
            self.setProperty_wrap('bmsAdd0021', str(bms_remain))
            self.setProperty_wrap('bmsAdd0022', str(bms_highvol_id))
            self.setProperty_wrap('bmsAdd0023', str(bms_highvol_vol))
            self.setProperty_wrap('bmsAdd0024', str(bms_lowvol_id))
            self.setProperty_wrap('bmsAdd0025', str(bms_lowvol_vol))
            self.setProperty_wrap('bmsAdd0026', str(bms_hightem_id))
            self.setProperty_wrap('bmsAdd0027', str(bms_hightem_tem))
            self.setProperty_wrap('bmsAdd0028', str(bms_lowtem_id))
            self.setProperty_wrap('bmsAdd0029', str(bms_lowtem_tem))
            self.split_nb_property(bms_state, ['', \
                                               'bmsAdd0001Bit1', \
                                               '', \
                                               'bmsAdd0001Bit3', \
                                               'bmsAdd0001Bit4', \
                                               'bmsAdd0001Bit5', \
                                               'bmsAdd0001Bit6'], 7)
            self.set_distinct_property_inc0(calc_comb_bit(bms_state, 2, 2), \
                                            ['bmsAdd0001Bit2Val0', 'bmsAdd0001Bit2Val1'])
            self.split_nb_property(bms_warning, ['bmsAdd0002Bit0', \
                                                 'bmsAdd0002Bit1', \
                                                 'bmsAdd0002Bit2', \
                                                 'bmsAdd0002Bit3', \
                                                 'bmsAdd0002Bit4', \
                                                 'bmsAdd0002Bit5', \
                                                 'bmsAdd0002Bit6', \
                                                 'bmsAdd0002Bit7', \
                                                 'bmsAdd0002Bit8', \
                                                 'bmsAdd0002Bit9'], 10)

    def packet_desalinplant(self, packet):
        packet_data_str = []
        if packet['MODBUS'].func_code == '3':
            pass
        else:
            return
        # TODO   '''           below              '''
        self.setProperty_wrap('desalinplantAdd1018', '否')
        self.setProperty_wrap('desalinplantAdd1002Bit0Val0', '否')
        self.setProperty_wrap('desalinplantAdd1002Bit0Val1', '是')
        self.setProperty_wrap('desalinplantAdd1002Bit0Val0', '是')
        self.setProperty_wrap('desalinplantAdd1001Bit0', '否')
        self.setProperty_wrap('desalinplantAdd1001Bit1', '是')
        self.setProperty_wrap('desalinplantAdd1001Bit2', '是')
        self.setProperty_wrap('desalinplantAdd1001Bit3', '否')
        self.setProperty_wrap('desalinplantAdd1001Bit4', '是')
        self.setProperty_wrap('desalinplantAdd1001Bit5', '否')
        self.setProperty_wrap('desalinplantAdd1001Bit6', '是')
        self.setProperty_wrap('desalinplantAdd1001Bit7', '是')  #
        self.setProperty_wrap('desalinplantAdd1003Bit0', '否')
        self.setProperty_wrap('desalinplantAdd1003Bit1', '否')
        self.setProperty_wrap('desalinplantAdd1003Bit2', '否')
        self.setProperty_wrap('desalinplantAdd1003Bit3', '否')
        self.setProperty_wrap('desalinplantAdd1003Bit4', '否')
        self.setProperty_wrap('desalinplantAdd1003Bit5', '否')
        self.setProperty_wrap('desalinplantAdd1003Bit6', '否')
        self.setProperty_wrap('desalinplantAdd1003Bit7', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit0', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit1', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit2', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit3', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit4', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit5', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit6', '否')
        self.setProperty_wrap('desalinplantAdd1004Bit7', '否')
        self.setProperty_wrap('desalinplantAdd1008', '0.4')
        self.setProperty_wrap('desalinplantAdd1019', '0.3')
        self.setProperty_wrap('desalinplantAdd1009', '0.5')
        self.setProperty_wrap('desalinplantAdd1004Bit7', '否')
        fzgl = random.randint(1, 10)
        newfzgl = float(fzgl / 10)
        realfzgl = newfzgl + 17
        self.setProperty_wrap('desalinplantAdd1007', str(realfzgl))
        yjcsdd = random.random()
        if yjcsdd <= 0.8:
            self.setProperty_wrap('desalinplantAdd1010', str(3.5))
        elif yjcsdd >= 0.3:
            self.setProperty_wrap('desalinplantAdd1010', str(3.6))
        else:
            self.setProperty_wrap('desalinplantAdd1010', str(3.4))
        ejcsdd = random.random()
        if ejcsdd <= 0.6:
            self.setProperty_wrap('desalinplantAdd1011', str(1.4))
        elif ejcsdd >= 0.4:
            self.setProperty_wrap('desalinplantAdd1011', str(1.3))
        else:
            self.setProperty_wrap('desalinplantAdd1011', str(1.2))
        ysxyw = random.randint(1, 10)
        if ysxyw >= 6:
            newysxyw = float(ysxyw / 10)
            realysxyw = newysxyw + 33
            self.setProperty_wrap('desalinplantAdd1013', str(realysxyw))
        else:
            self.setProperty_wrap('desalinplantAdd1013', str(33.5))
        ufsxyw = random.randint(1, 10)
        if ufsxyw <= 5:
            newufsxyw = float(ufsxyw / 10)
            realufsxyw = newufsxyw + 20
            self.setProperty_wrap('desalinplantAdd1014', str(realufsxyw))
        else:
            self.setProperty_wrap('desalinplantAdd1014', str(20.2))
        yjsxyw = random.randint(1, 10)
        if yjsxyw >= 6:
            newyjsxyw = float(yjsxyw / 10)
            realyjsxyw = newyjsxyw + 35
            self.setProperty_wrap('desalinplantAdd1015', str(realyjsxyw))
        else:
            self.setProperty_wrap('desalinplantAdd1015', str(35.5))
        ejsxyw = random.randint(1, 10)
        if ejsxyw >= 6:
            newejsxyw = float(ejsxyw / 10)
            realejsxyw = newejsxyw + 36
            self.setProperty_wrap('desalinplantAdd1016', str(realejsxyw))
        else:
            self.setProperty_wrap('desalinplantAdd1016', str(36.7))

    def setProperty_wrap(self, prop, value):
        self.sigUpdate.emit(prop, value)

    def set_distinct_property_inc0(self, data, prop):
        if data == 0:
            self.setProperty_wrap(prop[0], '是')
        else:
            self.setProperty_wrap(prop[0], '否')
        self.set_distinct_property(data, prop[1:])

    def set_distinct_property(self, data, prop):
        i = 0
        for it in prop:
            i += 1
            if it == '':
                continue
            if i == data:
                self.setProperty_wrap(it, '是')
            else:
                self.setProperty_wrap(it, '否')

    def split_8b_property(self, data, prop):
        self.split_nb_property(data, prop, 8)

    def split_16b_property(self, data, prop):
        self.split_nb_property(data, prop, 16)

    def split_nb_property(self, data, prop, n):
        mask = 1
        for i in range(n):
            if prop[i] == '':
                continue
            if data & (mask << i) != 0:
                self.setProperty_wrap(prop[i], '是')
            else:
                self.setProperty_wrap(prop[i], '否')

def calc_comb_bit(data, start, end):
    ret = 0
    j = 0
    for i in range(start, end + 1):
        ret += (1 if data & (1 << i) > 0 else 0) * (1 << j)
        j += 1
    return ret

if __name__ == '__main__':
    path = 'qml/main.qml'
    app = QGuiApplication([])
    view = QmlView()
    config.settings.sv2(1)  # 加在这里可以 让filedialog在python.exe窗口之后出来
    view.engine().quit.connect(app.quit)
    view.setSource(QUrl(path))
    view.show()
    app.exec_()
