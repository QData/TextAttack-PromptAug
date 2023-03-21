import matplotlib.pyplot as plt
import numpy as np

from shapely.geometry import Polygon, Point
from datasets.constants import *

class Shape:
    """
    Abstract class for shapes
    
    """
    def __init__(self, color, size):
        self.name = None
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        
        if color not in COLORS:
            raise ValueError()
        if size not in SIZES:
            raise ValueError()
        self.color = color
        self.size = size
    
    def get_plot_shape(self):
        return NotImplemented
    
    def get_intersection_shape(self):
        return NotImplemented
    
    def inbounds(self):
        return (
            self.left >= X_MIN and
            self.right <= X_MAX and
            self.bottom >= Y_MIN and 
            self.top <= Y_MAX
        )
    
    def intersect(self, other):
        return self.get_intersection_shape().intersects(other.get_intersection_shape())
    
    def get_color(self):
        return {
            "Red": "#d62728",
            "Blue": "#1f77b4",
            "Yellow": "#fce303",
            "Green": "#2ca02c",
        }[self.color]
    
    def to_json(self):
        return {
            "shape": self.name, 
            "color": self.color, 
            "size": self.size, 
            "center": self.center, 
        }


class Circle(Shape):
    def __init__(self, color, size, center):
        super().__init__(color, size)
        self.name = "Circle"
        self.center = center
        if self.size == "Small":
            radius = 1
        elif self.size == "Large":
            radius = 4
        self.radius = radius
        
        self.left = self.center[0] - self.radius
        self.right = self.center[0] + self.radius
        self.top = self.center[1] + self.radius
        self.bottom = self.center[1] - self.radius
        
    def get_plot_shape(self):
        return plt.Circle(self.center, self.radius, color=self.get_color())
    
    def get_intersection_shape(self):
        point = Point([self.center])
        return point.buffer(self.radius)
    

class Square(Shape):
    def __init__(self, color, size, center):
        super().__init__(color, size)
        self.name = "Square"
        self.center = center
        if self.size == "Small":
            length = 2
        elif self.size == "Large":
            length = 4
        self.length = length
        self.bottom_left = (
                self.center[0] - (self.length // 2), 
                self.center[1] - (self.length // 2))
        
        self.left = self.bottom_left[0]
        self.bottom = self.bottom_left[1]
        self.right = self.left + self.length
        self.top = self.bottom + self.length
        
    def get_plot_shape(self):
        return plt.Rectangle(self.bottom_left, self.length, self.length, color=self.get_color())
            
    def get_intersection_shape(self):
        return Polygon([
            self.bottom_left, 
            (self.bottom_left[0] + self.length, self.bottom_left[1]), 
            (self.bottom_left[0] + self.length, self.bottom_left[1] + self.length),
            (self.bottom_left[0], self.bottom_left[1] + self.length)
        ])

class Triangle(Shape):
    def __init__(self, color, size, center):
        super().__init__(color, size)
        self.name = "Triangle"
        self.center = center
        if self.size == "Small":
            length = 2
        elif self.size == "Large":
            length = 4
        self.length = length
        
        self.top_point = (self.center[0], self.center[1] + self.length / np.sqrt(3))
        self.bottom_left = (self.center[0] - self.length // 2, self.center[1] - self.length / (2 * np.sqrt(3)))
        self.bottom_right = (self.center[0] + self.length // 2, self.center[1] - self.length / (2 * np.sqrt(3)))
        
        self.top = self.top_point[1]
        self.bottom = self.bottom_left[1]
        self.left = self.bottom_left[0]
        self.right = self.bottom_right[0]
        
    def get_plot_shape(self):
        return plt.Polygon([
            self.top_point, self.bottom_left, self.bottom_right, 
        ], color=self.get_color())
            
    def get_intersection_shape(self):
        return Polygon([
            self.top_point, self.bottom_left, self.bottom_right
        ])
