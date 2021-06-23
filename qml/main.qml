﻿import QtQuick 2.5
import QtQuick.Window 2.2  //不论哪种加载方式都需要在这个window
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.3
 //一个数字占一个vchar 一个汉字占两个varchar


TabView {

//Import Statement:import QtQuick.Controls 1.4
     
    //Template
    property string var_nonbool: 'XXXX'
    property string var_bool: 'Y'


   //解析数据包的位置
   property string file_path: ' '



    //风电机组1 数值
    property string windturb1_40005: '0000'
    property string windturb1_40006: '0000'
    property string windturb1_40007: '0000'
    property string windturb1_40008: '0000'
    property string windturb1_40009: '0000'
    property string windturb1_40260: '0000'
    property string windturb1_40065: '0000'
    property string windturb1_40066: '0000'
    property string windturb1_40067: '0000'
    property string windturb1_40068: '0000'
    property string windturb1_40069: '0000'
    property string windturb1_40070: '0000'
    property string windturb1_40071: '0000'
    property string windturb1_40072: '0000'
    property string windturb1_40073: '0000'
    property string windturb1_40075: '0000'

    property string windturb1_40261: '0000'

    //风电机组1 布尔
    property string windturb1_40001_1: '-'
    property string windturb1_40003_1: '-'
    property string windturb1_40001_2: '-'
    property string windturb1_40003_2: '-'
    property string windturb1_40002_1: '-'
    property string windturb1_40003_3: '-'
    property string windturb1_40002_2: '-'
    property string windturb1_40003_4: '-'
    property string windturb1_40002_3: '-'
    property string windturb1_40003_5: '-'
    property string windturb1_40002_4: '-'
    property string windturb1_40003_6: '-'

  

    property string windturb1_40010_2: '-'
    property string windturb1_40010_5: '-'
    property string windturb1_40010_0: '-'
    property string windturb1_40010_3: '-'
    property string windturb1_40010_6: '-'
    property string windturb1_40010_1: '-'
    property string windturb1_40010_4: '-'
    property string windturb1_40010_7: '-'

    property string windturb1txgz: '-'

    //=======================================
    //风电机组2 数值
    property string windturb2Add0000: '0000'
    property string windturb2Add0001: '0000'
    property string windturb2Add0002: '0000'
    property string windturb2Add0003: '0000'
    property string windturb2Add0004: '0000'
    property string windturb2Add0005: '0000'
    property string windturb2Add0006: '0000'
    property string windturb2Add0007: '0000'
    property string windturb2Add0008_low: '0000'
    property string windturb2Add0009_high: '0000'
    property string windturb2Add0008plus9: '0000'
    property string windturb2Add0010: '0000'       
/*qt qml中数字不能作为变量的开头第一个字母！！*/
    //风电机组2 布尔
    property string w2_4X0032bit0sdzt: '-'
    property string w2_4X0032bit1zdzt: '-'
    property string w2_4X0032bit2djzt: '-'
    property string w2_4X0032bit3yxzt: '-'
    property string w2_4X0032bit4tjzt: '-'
    property string w2_4X0032bit5jdzt: '-'
    property string w2_4X0032bit6yczt: '-'
    property string w2_4X0032bit7vain: '-'

    property string w2_4X0033bit0djcs: '-'
    property string w2_4X0033bit1dfbj: '-'
    property string w2_4X0033bit2djgz: '-'
    property string w2_4X0033bit3nbqgz:'-'
    property string w2_4X0033bit4phgz: '-'
    property string w2_4X0033bit5bjgz: '-'
    property string w2_4X0033bit6ywgz: '-'
    property string w2_4X0033bit7txgz: '-'
    //=======================================
    //储能双向变流器 数值
    property string pcsAdd2000: '0000'
    property string pcsAdd2001: '0000'
    property string pcsAdd2002: '0000'
    property string pcsAdd2003: '0000'
    property string pcsAdd2004: '0000'
    property string pcsAdd2005: '0000'
    property string pcsAdd2006: '0000'
    property string pcsAdd2007: '0000'
    property string pcsAdd2008: '0000'
    property string pcsAdd2009: '0000'
    property string pcsAdd2010: '0000'
    property string pcsAdd2011: '0000'
    //储能双向变流器 布尔
    property string pcsAdd2012Bit0Val0: '-'
    property string pcsAdd2012Bit0Val1: '-'
    property string pcsAdd2012Bit0Val2: '-'
    property string pcsAdd2012Bit4Val0: '-'
    property string pcsAdd2012Bit4Val2: '-'
    property string pcsAdd2012Bit12Val0: '-'
    property string pcsAdd2012Bit12Val1: '-'
    property string pcsAdd2012Bit12Val2: '-'
    property string pcsAdd2012Bit12Val3: '-'
    property string pcsAdd2012Bit12Val4: '-'
    property string pcsAdd2012Bit12Val5: '-'
    property string pcsAdd2014Bit0: '-'
    property string pcsAdd2014Bit1: '-'
    property string pcsAdd2014Bit2: '-'
    property string pcsAdd2014Bit3: '-'
    property string pcsAdd2014Bit4: '-'
    property string pcsAdd2014Bit5: '-'
    property string pcsAdd2014Bit6: '-'
    property string pcsAdd2014Bit7: '-'
    property string pcsAdd2014Bit8: '-'
    property string pcsAdd2014Bit9: '-'
    property string pcsAdd2014Bit10: '-'
    property string pcsAdd2014Bit11: '-'
    property string pcsAdd2014Bit12: '-'
    property string pcsAdd2014Bit13: '-'
    property string pcsAdd2014Bit14: '-'
    property string pcsAdd2014Bit15: '-'
    property string pcsAdd2015Bit0: '-'
    //=======================================
    //电池组 数值
    property string bmsAdd0004: '0000' //1组电压值
    property string bmsAdd0005: '0000' //2组电压值
    property string bmsAdd0006: '0000'  //总电压值
    property string bmsAdd0007: '0000'  //1组电流值  
    property string bmsAdd0008: '0000'   //2组电流值
    property string bmsAdd0009: '0000'
    property string bmsAdd0010: '0000'
    property string bmsAdd0011: '0000'
    property string bmsAdd0012: '0000'
    property string bmsAdd0013: '0000'
    property string bmsAdd0014: '0000'
    property string bmsAdd0015: '0000'
    property string bmsAdd0016: '0000'
    property string bmsAdd0017: '0000'
    property string bmsAdd0018: '0000'
    property string bmsAdd0019: '0000'
    property string bmsAdd0020: '0000'
    property string bmsAdd0021: '0000'
    property string bmsAdd0022: '0000'
    property string bmsAdd0023: '0000'
    property string bmsAdd0024: '0000'
    property string bmsAdd0025: '0000'
    property string bmsAdd0026: '0000'
    property string bmsAdd0027: '0000'
    property string bmsAdd0028: '0000'
    property string bmsAdd0029: '0000'
    //电池组 布尔
    property string bmsAdd0001Bit1: '-'
    property string bmsAdd0001Bit2Val0: '-'
    property string bmsAdd0001Bit2Val1: '-'
    property string bmsAdd0001Bit3: '-'
    property string bmsAdd0001Bit4: '-'
    property string bmsAdd0001Bit5: '-'
    property string bmsAdd0001Bit6: '-'
    property string bmsAdd0002Bit0: '-'
    property string bmsAdd0002Bit1: '-'
    property string bmsAdd0002Bit2: '-'
    property string bmsAdd0002Bit3: '-'
    property string bmsAdd0002Bit4: '-'
    property string bmsAdd0002Bit5: '-'
    property string bmsAdd0002Bit6: '-'
    property string bmsAdd0002Bit7: '-'
    property string bmsAdd0002Bit8: '-'
    property string bmsAdd0002Bit9: '-'
    //=======================================
    //海水淡化 数值
    property string desalinplantAdd1007: '00.0'   //负载功率(kW)
    property string desalinplantAdd1008: '0.0'     // 一级产水流量(t/h)
    property string desalinplantAdd1009: '0.0'   //   产水量(吨/小时)
    property string desalinplantAdd1010: '0.0'     //一级产水电导(uS/cm)
    property string desalinplantAdd1011: '0.0'    //二级产水电导(uS/cm)
    property string desalinplantAdd1013: '0.0'  //原水箱液位(cm)
    property string desalinplantAdd1014: '0.0' //UF产水箱液位(cm)
    property string desalinplantAdd1015: '0.0'      //一级产水箱液位(cm)
    property string desalinplantAdd1016: '0.0'  //二级产水箱液位(cm)
    property string desalinplantAdd1018: '-'   // 通讯报警
    property string desalinplantAdd1019: '0.0'                        //二级产水流量(t/h)
    //海水淡化 布尔
    property string desalinplantAdd1002Bit0Val0: '-'   //就地
    property string desalinplantAdd1002Bit0Val1: '-'    //远程
    property string desalinplantAdd1001Bit0: '-'          //系统正常
    property string desalinplantAdd1001Bit1: '-'        //启动过程
    property string desalinplantAdd1001Bit2: '-'    //正常运行
    property string desalinplantAdd1001Bit3: '-'      //正常停机过程中
    property string desalinplantAdd1001Bit4: '-'         //停机结束
    property string desalinplantAdd1001Bit5: '-'      //非正常停机
    property string desalinplantAdd1001Bit6: '-'    //淡水冲洗
    property string desalinplantAdd1001Bit7: '-'         //淡水冲洗结束


    property string desalinplantAdd1003Bit0: '-'   //以下都是故障报警
    property string desalinplantAdd1003Bit1: '-'
    property string desalinplantAdd1003Bit2: '-'
    property string desalinplantAdd1003Bit3: '-'
    property string desalinplantAdd1003Bit4: '-'
    property string desalinplantAdd1003Bit5: '-'
    property string desalinplantAdd1003Bit6: '-'
    property string desalinplantAdd1003Bit7: '-'
    property string desalinplantAdd1004Bit0: '-'
    property string desalinplantAdd1004Bit1: '-'
    property string desalinplantAdd1004Bit2: '-'
    property string desalinplantAdd1004Bit3: '-'
    property string desalinplantAdd1004Bit4: '-'
    property string desalinplantAdd1004Bit5: '-'
    property string desalinplantAdd1004Bit6: '-'
    property string desalinplantAdd1004Bit7: '-'

    //ADAM1
    property string adam1di0:'-'   //柴发断路器状态位 adam1di0str
    property string adam1di1:'-'   //风机1断路器状态位 adam1di1str
    property string adam1di2:'-'   //风机2断路器状态位 adam1di2str
    property string adam1di3:'-'

    property string adam1di4:'-'     //PCS断路器状态位 adam1di4str
    property string adam1di5:'-'     //电气柜UPS断路器状态位 adam1di5str
    property string adam1di6:'-'   //电气柜UPS故障状态位 adam1di6str
    property string adam1di7:'-'   //电气柜UPS报警状态位 adam1di7str

    property string adam1di8:'-'    //居民断路器状态位 adam1di8str
    property string adam1di9:'-'    
    property string adam1di10:'-'   //空调断路器状态位 adam1di10str
    property string adam1di11:'-'
    property string adam1di0str:'--' 
 property string adam1di1str:'--'
 property string adam1di2str:'--'
 property string adam1di3str:'--'
 property string adam1di4str:'--'
 property string adam1di5str:'--'
 property string adam1di6str:'--'
 property string adam1di7str:'--'
 property string adam1di8str:'--'
 property string adam1di9str:'--'
 property string adam1di10str:'--'
 property string adam1di11str:'--'


    property string adam1do0:'-'  //柴发中间继电器状态位 adam1do0str
    property string adam1do1:'-'   //居民中间继电器状态位 adam1do1str
    property string adam1do2:'-'     
    property string adam1do3:'-'  //空调中间继电器状态位 adam1do3str
    property string adam1do4:'-' 
    property string adam1do5:'-'  //照明中间继电器状态位 adam1do5str
    property string adam1do6:'-'
    property string adam1do7:'-'

 property string adam1do0str:'--'
 property string adam1do1str:'--'
 property string adam1do2str:'--'
 property string adam1do3str:'--'
 property string adam1do4str:'--'
 property string adam1do5str:'--'
 property string adam1do6str:'--'
 property string adam1do7str:'--'

     //ADAM2

    property string adam2di0:'-'  
    property string adam2di1:'-'
    property string adam2di2:'-'  
    property string adam2di3:'-'

    property string adam2di4:'-'
    property string adam2di5:'-'
    property string adam2di6:'-'
    property string adam2di7:'-'

    property string adam2di8:'-'
    property string adam2di9:'-'
    property string adam2di10:'-'
    property string adam2di11:'-'
    property string adam2di0str:'--'  //照明断路器状态 adam2di0str
 property string adam2di1str:'--'    
 property string adam2di2str:'--'      // 空调热继状态 adam2di2str
 property string adam2di3str:'--'
 property string adam2di4str:'--'     //照明热继状态  adam2di4str
 property string adam2di5str:'--'
 property string adam2di6str:'--'    //空调接触器状态 adam2di6str
 property string adam2di7str:'--'
 property string adam2di8str:'--'     //照明接触器状态 adam2di8str
 property string adam2di9str:'--'
 property string adam2di10str:'--'   //滤波器断路器状态 adam2di10str
 property string adam2di11str:'--'


    property string adam2do0:'-'
    property string adam2do1:'-'
    property string adam2do2:'-'
    property string adam2do3:'-'
    property string adam2do4:'-'
    property string adam2do5:'-'
    property string adam2do6:'-'
    property string adam2do7:'-'

 property string adam2do0str:'--'
 property string adam2do1str:'--'
 property string adam2do2str:'--'
 property string adam2do3str:'--'
 property string adam2do4str:'--'
 property string adam2do5str:'--'
 property string adam2do6str:'--'
 property string adam2do7str:'--'


     //ADAM3
    property string adam3di0:'-'
    property string adam3di1:'-'
    property string adam3di2:'-'
    property string adam3di3:'-'

    property string adam3di4:'-'
    property string adam3di5:'-'
    property string adam3di6:'-'
    property string adam3di7:'-'

    property string adam3di8:'-'
    property string adam3di9:'-'
    property string adam3di10:'-'
    property string adam3di11:'-'

    property string adam3di0str:'--'
 property string adam3di1str:'--'
 property string adam3di2str:'--'
 property string adam3di3str:'--'
 property string adam3di4str:'--'
 property string adam3di5str:'--'
 property string adam3di6str:'--'
 property string adam3di7str:'--'
 property string adam3di8str:'--'
 property string adam3di9str:'--'
 property string adam3di10str:'--'
 property string adam3di11str:'--'


    property string adam3do0:'-'
    property string adam3do1:'-'
    property string adam3do2:'-'
    property string adam3do3:'-'
    property string adam3do4:'-'
    property string adam3do5:'-'
    property string adam3do6:'-'
    property string adam3do7:'-'

 property string adam3do0str:'--'
 property string adam3do1str:'--'
 property string adam3do2str:'--'
 property string adam3do3str:'--'
 property string adam3do4str:'--'
 property string adam3do5str:'--'
 property string adam3do6str:'--'
 property string adam3do7str:'--'


    id: root
    width:720
    height: 480
   


    Tab {
        title: "风电机组1"
        WINDTURB1 {}
        /*source: "WINDTURB1.qml"*/
    }
 Tab {
        title: "风电机组2"
        WINDTURB2 {}
    }
    Tab {
        
        title: "储能双向变流器"


        EMS{}
        //对应PowerSystem.qml
    }

 Tab {
        title: "电池组"
       BMS{}
    }
 

    Tab {
        title: "反渗透海水淡化装置"
        DesalinPlant {}
    }


Tab {
        title: "ADAM1"
        ADAM1 {}
        }

 Tab {
        title: "ADAM2"
        ADAM2 {}
     }

 Tab {
        title: "ADAM3"
        ADAM3 {}
     }
   style: TabViewStyle {
        frameOverlap: 1
        tab: Rectangle {
            color: styleData.selected ? "steelblue" :"lightsteelblue"
            border.color:  "steelblue"
            implicitWidth: Math.max(text.width + 4, 80)
            implicitHeight: 20
            radius: 2
            Text {
                id: text
                anchors.centerIn: parent
                text: styleData.title
                color: styleData.selected ? "white" : "black"
            }
        }
        frame: Rectangle { color: "steelblue" }
    }


  

}
