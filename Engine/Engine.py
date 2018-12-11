import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QPoint, QRect, Qt, QThread
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QScreen
from PyQt5.QtWidgets import QApplication, QWidget

from World import World

class Engine(QWidget):

    class RunThread(QThread):
        def __init__(self, engine):
            QtCore.QThread.__init__(self) 
            self.engine = engine
            self.running = True
        
        def run(self):
            while self.running:
                start_time = time.time()

                self.engine.active_world.runEntities()
                self.engine.active_world.run()
                
                if(1/60 - (time.time() - start_time)) > 0:
                    time.sleep(1/60 - (time.time() - start_time))

    def __init__(self):
        super().__init__()

        self.setFixedSize(QScreen.size(QApplication.primaryScreen()).width(), 
                          QScreen.size(QApplication.primaryScreen()).height())
        #set scale based on relation to 1080p
        self.scale = QScreen.size(QApplication.primaryScreen()).width()/1080
        self.showFullScreen()

        self.active_world = World(self)
        
        self.run_thread = self.RunThread(self)
        self.run_thread.start()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        qp.drawImage(QPoint(0,0), self.active_world.background)
        self.active_world.drawScreen(qp)
        
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Engine()
    sys.exit(app.exec_())
