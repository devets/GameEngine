from Entity import Entity
from ActiveEntity import ActiveEntity

from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QImage
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer

class World():

    def __init__(self, engine):
        self.__entity_list = []

        self.__engine = engine
        self.Screen = Entity()
        self.Screen.x = 0
        self.Screen.y = 0
        self.Screen.width = self.__engine.screen_width
        self.Screen.height = self.__engine.screen_height

        # View offset for the camera to facilitate scrolling
        # These are added to the x and y value of each entity when rendered

        #default white background
        self.background = QImage(self.Screen.width, self.Screen.height, QImage.Format_RGB32)
        self.background.fill(QColor(255,255,255))

    def drawScreen(self, qp):
        """Draws all entities to the screen.\n
        qp -- a QPainter.
        """
        for e in self.__entity_list:
            if e.image != None:
                if (e.isTouching(self.Screen)):
                    qp.drawImage(QPoint(int(e.x * self.__engine.scale),
                                 int(e.y * self.__engine.scale)),
                                 e.getImage(self.__engine.scale))

    def runEntities(self):
        """Calls the physics() and run() methods."""
        for e in self.__entity_list:
            if isinstance(e, ActiveEntity):
                e.physics()
                e.run()

    def run(self):
        """User implementation of run method."""
        pass


    def addEntity(self, entity, x, y):
        """Add the designated entity to the entity list.\n
        x -- x-coordinate of the entity\n
        y -- y-coordinate of the entity
        """
        if not isinstance(entity, Entity):
            raise TypeError("Only accepts objects of type Entity")
        entity.x = x
        entity.y = y
        self.__entity_list.append(entity)

    def removeEntity(self, entity):
        """Remove the designated entity from the entity list."""
        self.__entity_list.remove(entity)
