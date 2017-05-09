#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Piste: ({self.x}, {self.y})"

class Circle:
    def __init__(self, r):
        self.r = r

    def getCenter(self):
        return Point(self.r, self.r)

    def isPointIn(self, p):
        center = self.getCenter()
        return math.sqrt((p.x - center.x) ** 2 + (p.y - center.y) ** 2) < self.r

    def __str__(self):
        return f"Ympyrä: säde: {self.r}"

circle = Circle(10.0)
point1 = Point(2.0, 5.0)
point2 = Point(0.1, 0.001)

print(circle)
print(point1)
print(point2)

print(circle.isPointIn(point1), circle.isPointIn(point2))

