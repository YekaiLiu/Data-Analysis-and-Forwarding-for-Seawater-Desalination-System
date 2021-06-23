import QtQuick 2.0
PageView{

    id:adam1
    property alias text1: text1
    property alias text2: text2
    Rectangle{
               width:adam1.width
               height:adam1.height
               color: '#eeeeee'
              
               //color: 'blue'
               Text {
                   id: text1
                          text: "微网系统电控柜硬件点表1"
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
                          text: "ADAM-6050-1"
                          font.pixelSize: 20
                          color: "#0091ea"
                      }
                      Text {
                          x: 10
                          y: 75
                          text: "柴发断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 75
                         
                           text:root.adam1di0str
                          font.pixelSize: 15
                          color: "#212121"
                      }




                      Text {
                          x: 10
                          y: 95
                          text: "风机1断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }


                      Text {
                          x: 10+150
                          y: 95
                          text: root.adam1di1str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10
                          y: 115
                          text: "风机2断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 115
                          text:  root.adam1di2str
                          font.pixelSize: 15
                          color: "#212121"
                      }



                      Text {
                          x: 10
                          y: 155
                          text: "PCS断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 155
                          text: root.adam1di4str
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10
                          y: 175
                          text: "电气柜UPS断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10+150
                          y: 175
                          text: root.adam1di5str
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10
                          y: 195
                          text: "电气柜UPS故障"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 195
                          text: root.adam1di6str
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10
                          y: 215
                          text: "电气柜UPS报警"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 215
                          text: root.adam1di7str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10
                          y: 235
                          text: "居民断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 235
                          text: root.adam1di8str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 10
                          y: 255
                          text: "空调断路器状态"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 10+150
                          y: 255
                          text: root.adam1di10str
                          font.pixelSize: 15
                          color: "#212121"
                      }


                      Text {
                          x: 400
                          y: 75
                          text: "柴发中间继电器"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 400+150
                          y: 75
                         
                           text:root.adam1do0str
                          font.pixelSize: 15
                          color: "#212121"
                      }




                      Text {
                          x: 400
                          y: 95
                          text: "居民中间继电器"
                          font.pixelSize: 15
                          color: "#212121"
                      }


                      Text {
                          x: 400+150
                          y: 95
                          text: root.adam1do1str
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 400
                          y: 115
                          text: "空调中间继电器"
                          font.pixelSize: 15
                          color: "#212121"
                      }
                      Text {
                          x: 400+150
                          y: 115
                          text:  root.adam1do3str
                          font.pixelSize: 15
                          color: "#212121"
                      }



                      Text {
                          x: 400
                          y: 155
                          text: "照明中间继电器"
                          font.pixelSize: 15
                          color: "#212121"
                      }

                      Text {
                          x: 400+150
                          y: 155
                          text: root.adam1do5str
                          font.pixelSize: 15
                          color: "#212121"
                      }

             Image {
            opacity: 0.25
            anchors.fill: parent
            source: "b6.jpg"          //只能放在最后面不然容易卡

         }       
             }
    }
