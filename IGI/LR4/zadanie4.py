from abc import ABC
from abc import abstractmethod
import math
import matplotlib.pyplot

class GeometicFigure(ABC):
    @abstractmethod
    def area(self):
        pass    
    def translate(self,angle):
        return math.radians(angle)

class FigureColor:
    def __init__(self, color:str):
        self._color = color

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color:str):
        self._color = color    

class Triangle(GeometicFigure, FigureColor):
    def __init__(self, height, base, color, angle):
        self._base = base
        self._height = height
        self._angle = angle
        self.name = "Triangle"
        FigureColor.__init__(self, color)

    def area(self):
        return self._base * self._height * 0.5

    def info(self):
        return "{}: Base = {}, Height = {}, Color = {}, Angle = {}  Area = {:.2f}".format(
            self.name, self._base, self._height, self._color, self._angle, self.area()
        )
    
    def draw(self, text):
        angleR = super().translate(self._angle)#####
        c = self._height / math.sin(angleR)
        baseA = math.sqrt(((c**2))-self._height**2) 
        x = [
            0,baseA,self._base
        ]
        y = [0, self._height, 0]
        matplotlib.pyplot.figure()
        matplotlib.pyplot.fill(
            x, y, color=self._color.lower() , edgecolor = "black" 
        )
        matplotlib.pyplot.axis("equal")
        matplotlib.pyplot.title(text)
        matplotlib.pyplot.savefig(r"C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\triangle.png")