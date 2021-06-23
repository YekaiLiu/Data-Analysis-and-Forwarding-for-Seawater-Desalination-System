import QtQuick 2.0
PageView{

    id:adam2
    property alias text1: text1
    property alias text2: text2
    Rectangle{
               width:adam2.width
               height:adam2.height
               color: '#eeeeee'
               Text {
                   id: text1
                          text: "微网系统电控柜硬件点表2"
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
                          text: "ADAM-6050-2"
                          font.pixelSize: 20
                          color: "#0091ea"
                      }
                      Text {
                          x: 10
                          y: 75
                          text: "照明断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 75
                    
                           text:root.adam2di0str
                          font.pixelSize: 15
                          color: "#212121"
                      }




                      Text {
                          x: 10
                          y: 95
                          text: "空调热继状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }


                      Text {
                          x: 10+150
                          y: 95
                          text: root.adam2di2str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10
                          y: 115
                          text: "照明热继状态"
                          font.pixelSize: 15
                          color: "#212121"
                        }
                      Text {
                          x: 10+150
                          y: 115
                          text:  root.adam2di4str
                          font.pixelSize: 15
                          color: "#212121"
                      }



                      Text {
                          x: 10
                          y: 155
                          text: "空调接触器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 155
                          text: root.adam2di6str
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10
                          y: 175
                          text: "照明接触器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 175
                          text: root.adam2di8str
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10
                          y: 195
                          text: "滤波器断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 195
                          text: root.adam2di10str
                          font.pixelSize: 15
                          color: "#212121"
                      }

Image {
            opacity: 0.25
            anchors.fill: parent
            source: "b7.png"          //只能放在最后面不然容易卡

         }

             }
    }
