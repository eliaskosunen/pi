#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import random
import time
import csv
import argparse

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def createRandom(circle):
        return Point(
            random.uniform(
                0,
                2 * circle.r),
            random.uniform(
                0,
             2 * circle.r))

    def __str__(self):
        return f"Point: ({self.x}, {self.y})"


class Circle:

    def __init__(self, r):
        self.r = r

    def getCenter(self):
        return Point(self.r, self.r)

    def isPointIn(self, p):
        center = self.getCenter()
        return (p.x - center.x) ** 2 + (p.y - center.y) ** 2 < self.r ** 2

    def __str__(self):
        return f"Circle: radius: {self.r}"


def powers_of_ten(begin, end):
    begin_pow = 10 ** begin
    end_pow = 10 ** end + 1
    while begin_pow < end_pow:
        yield begin_pow
        begin_pow *= 10


def area(circle, pointCount):
    points = pointCount*[None]
    pointsInCircle = 0

    for i in range(pointCount):
        point = Point.createRandom(circle)
        points[i] = point
        if circle.isPointIn(point):
            pointsInCircle += 1

    return points, pointsInCircle


def percentage_diff(val1, val2):
    return 100 * math.fabs(val1 - val2) / ((val1 + val2) / 2)

parser = argparse.ArgumentParser()
parser.add_argument("--write-points", action='store_true')
cmdargs = parser.parse_args()

def run(circle, pointCount, loop, squareArea):
    points, pointsInThisCircle = area(circle, pointCount)

    if cmdargs.write_points is not None:
        with open(f"points/points_{radius}_{pointCount}_{loop + 1}.csv",
                "w", newline='') as pointcsvfile:
            pointcsv = csv.DictWriter(pointcsvfile, fieldnames=['x', 'y'])
            pointcsv.writeheader()
            for pointid, pointval in enumerate(points):
                pointcsv.writerow({'x': pointval.x, 'y': pointval.y})

    return pointsInThisCircle, (pointsInThisCircle / pointCount * squareArea)

with open("results.csv", "w", newline='') as resultscsvfile:
    resultFieldnames = ['radius',
                        'loops',
                        'pointCount',
                        'pointsInCircleAvg',
                        'pointsInCircleAvgPercentage',
                        'deducedCircleArea',
                        'realCircleArea',
                        'errorPercentage',
                        'piEstimate',
                        'piErrorPercentage',
                        'timeMicroseconds']
    resultcsv = csv.DictWriter(resultscsvfile, fieldnames=resultFieldnames)
    resultcsv.writeheader()

    for radius in powers_of_ten(0, 3):
        circle = Circle(float(radius))
        print(64 * '-')
        print(circle)

        circleArea = math.pi * circle.r ** 2
        squareArea = (circle.r * 2) ** 2

        for pointCount in powers_of_ten(1, 6):
            print(pointCount)
            circleAreaProb = []
            pointsInCircle = []
            loops = 5
            timeStart = time.perf_counter()
            for loop in range(loops):
                p, c = run(circle, pointCount, loop, squareArea)
                pointsInCircle.append(p)
                circleAreaProb.append(c)

            circleAreaProbAvg = sum(circleAreaProb) / float(len(circleAreaProb))
            pointsInCircleAvg = sum(pointsInCircle) / float(len(pointsInCircle))

            pointsInCircleAvgPercentage = 100 * pointsInCircleAvg / pointCount
            errorPercentage = percentage_diff(circleArea, circleAreaProbAvg)
            piEstimate = pointsInCircleAvg / pointCount * 4;
            piErrorPercentage = percentage_diff(math.pi, piEstimate)

            timeEnd = time.perf_counter()
            timeDiff = timeEnd - timeStart
            timeDiffMs = timeDiff * 1000.0
            timeDiffYs = timeDiffMs * 1000.0

            data = {'radius': radius,
                    'loops': loops,
                    'pointCount': pointCount,
                    'pointsInCircleAvg': pointsInCircleAvg,
                    'pointsInCircleAvgPercentage':
                        pointsInCircleAvgPercentage,
                    'deducedCircleArea': circleAreaProbAvg,
                    'realCircleArea': circleArea,
                    'errorPercentage': errorPercentage,
                    'piEstimate': piEstimate,
                    'piErrorPercentage': piErrorPercentage,
                    'timeMicroseconds': timeDiffYs}
            assert len(data) == len(resultFieldnames)

            resultcsv.writerow(data)
