from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication

from QmlView import QmlView
import config.settings   #这个必须要加！
if __name__ == '__main__':
    path = 'qml/main.qml'   
    app = QGuiApplication([])
    
    view = QmlView()
    config.settings.sv2(1) 
    view.engine().quit.connect(app.quit)   
    view.setSource(QUrl(path))             
    view.show()

    app.exec_()                         
