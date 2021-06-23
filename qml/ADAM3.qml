import QtQuick 2.0

PageView{

    id:adam3
    property alias text1: text1
    property alias text2: text2
    Rectangle{
               width:adam3.width
               height:adam3.height
               color: '#eeeeee'
               Text {
                   id: text1
                          text: "微网系统电控柜硬件点表3"
                          font.pixelSize: 30
                          color: "#212121"
                          anchors.horizontalCenter: parent.horizontalCenter
                          anchors.top: parent.top
                          anchors.margins: 5
                    }






                      Text {
                          id: text2
                          x: 10
                          y: 50
                          text: "ADAM-6050-3"
                          font.pixelSize: 20
                          color: "#0091ea"
                      }
                      Text {
                          x: 10
                          y: 75
                          text: "浪涌保护状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 75
                        
                           text:root.adam3di0str
                          font.pixelSize: 15
                          color: "#212121"
                      }




                      Text {
                          x: 10
                          y: 95
                          text: "220V供电总空开状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }


                      Text {
                          x: 10+150
                          y: 95
                          text: root.adam3di1str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10
                          y: 115
                          text: "220/24V开关电源状态"
                          font.pixelSize: 15
                          color: "#212121"
                        }
                      Text {
                          x: 10+150
                          y: 115
                          text:  root.adam3di2str
                          font.pixelSize: 15
                          color: "#212121"
                      }



                      Text {
                          x: 10
                          y: 155
                          text: "24V空开状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 155
                          text: root.adam3di3str
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10
                          y: 175
                          text: "散热/除湿空开状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 175
                          text: root.adam3di4str
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10
                          y: 195
                          text: "控制柜UPS1报警"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 195
                          text: root.adam3di5str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10
                          y: 215
                          text: "控制柜UPS2报警"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 215
                          text: root.adam3di6str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10
                          y: 235
                          text: "海淡负载断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 235
                          text: root.adam3di7str
                          font.pixelSize: 15
                          color: "#212121"
                      }

Image {
            opacity: 0.25
            anchors.fill: parent
            source: "b8.png"          //只能放在最后面不然容易卡

         }



             }
    }
