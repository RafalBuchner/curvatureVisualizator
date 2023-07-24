import math
def dp(p,s=10):
    x, y = p
    r = s/2
    oval(x-r,y-r,s,s)

def drawBezier(*points):
    newPath()
    moveTo(points[0])
    if len(points) == 4:
        curveTo(*points[1:])
    elif len(points) == 3:
        qCurveTo(*points[1:])
    elif len(points) == 2:
        lineTo(*points[1:])
    drawPath()
    
def interpolateSetSOfValues(valuesA, valuesB, t):
    assert len(valuesA) == len(valuesB)
    interpolatedValues = []
    for idx, valueA in enumerate(valuesA):
        valueB = valuesB[idx]
        interpolatedValues.append(interpolation(valueA,valueB,t))
    return interpolatedValues
####


def rotatePoint(P, alfa, originPoint):
    """Rotates x/y around x_orig/y_orig by angle and returns result as [x,y]."""
    # alfa = math.radians(alfa)
    px, py = P
    originPointX, originPointY = originPoint

    x = (
        (px - originPointX) * math.cos(alfa)
        - (py - originPointY) * math.sin(alfa)
        + originPointX
    )
    y = (
        (px - originPointX) * math.sin(alfa)
        + (py - originPointY) * math.cos(alfa)
        + originPointY
    )

    return x, y
    
def calcAngle(A, B):
    """returns angle between line AB and axis x"""
    ax, ay = A
    bx, by = B
    xDiff = bx-ax
    yDiff = by-ay
    start = A
    end = B
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    return angle

def calculateTangentAngle(t, *points):
    """Calculates tangent angle for curve's/lines's current t-factor"""
    if len(points) == 4:
        xB, yB = derivativeBezier(t, *points)
    if len(points) == 3:
        xB, yB = derivativeQBezier(t, *points)
    if len(points) == 2:
        xB, yB = points[-1]

    return angle((0, 0), (xB, yB))

def interpolation(v1, v2, t):
    """one-dimentional bezier curve equation for interpolating"""
    vt = v1 * (1 - t) + v2 * t
    return vt
    
def calcSeg(t, *points):
    assert isinstance(t, float), "calcSeg ERROR: t is not a float"
    if len(points) == 2:
        a, b = points
        point = calcLine(t, a, b)
    if len(points) == 3:
        a, b, c = points
        point = calcQuadraticBezier(t, a, b, c)
    if len(points) == 4:
        a, b, c, d = points
        point = calcCubicBezier(t, a, b, c, d)

    return point

def calcCubicBezier(t, *pointList):
    """returns coordinates for factor called "t"(from 0 to 1). Based on cubic bezier formula."""
    assert len(pointList) == 4 and isinstance(t, float)
    p1x, p1y = pointList[0]
    p2x, p2y = pointList[1]
    p3x, p3y = pointList[2]
    p4x, p4y = pointList[3]

    x = (
        p1x * (1 - t) ** 3
        + p2x * 3 * t * (1 - t) ** 2
        + p3x * 3 * t**2 * (1 - t)
        + p4x * t**3
    )
    y = (
        p1y * (1 - t) ** 3
        + p2y * 3 * t * (1 - t) ** 2
        + p3y * 3 * t**2 * (1 - t)
        + p4y * t**3
    )

    return x, y

def calcQuadraticBezier(t, *pointList):
    assert len(pointList) == 3 and isinstance(t, float)
    p1x, p1y = pointList[0]
    p2x, p2y = pointList[1]
    p3x, p3y = pointList[2]
    x = (1 - t) ** 2 * p1x + 2 * (1 - t) * t * p2x + t**2 * p3x
    y = (1 - t) ** 2 * p1y + 2 * (1 - t) * t * p2y + t**2 * p3y
    return x, y

def calcLine(t, *pointList):
    """returns coordinates for factor called "t"(from 0 to 1). Based on cubic bezier formula."""
    assert len(pointList) == 2 and isinstance(t, float)

    p1x, p1y = pointList[0]
    p2x, p2y = pointList[1]

    x = interpolation(p1x, p2x, t)
    y = interpolation(p1y, p2y, t)

    return x, y

def calcDeriverate(*points):
    if len(points) == 4:
        (p1x,p1y),(p2x,p2y),(p3x,p3y),(p4x,p4y) = points
        a = 3*(p2x-p1x), 3*(p2y-p1y)
        b = 3*(p3x-p2x), 3*(p3y-p2y)
        c = 3*(p4x-p3x), 3*(p4y-p3y)
        return (a, b, c)
        
    elif len(points) == 3:
        (p1x,p1y),(p2x,p2y),(p3x,p3y) = points
        a = 2*(p2x-p1x), 2*(p2y-p1y)
        b = 2*(p3x-p2x), 2*(p3y-p2y)
        return (a, b)
        
    elif len(points) == 2:
        (p1x,p1y),(p2x,p2y) = points
        a = (p2x-p1x), (p2y-p1y)
        return (a)

def calcCurvatureAtT(t, *points):
    if len(points) == 2:
        return 0
    d = calcDeriverate(*points) # 1st derivative
    dd = calcDeriverate(*d) # 2nd derivative
    dx, dy = calcSeg(t, *d)
    ddx, ddy = calcSeg(t, *dd)
    num = dx * ddy - ddx * dy
    dnom = math.pow(dx*dx + dy*dy, 3/2)
    if num == 0 or dnom == 0: 
        return 0
    return num / dnom # kappa

def calcCurvatureAtTA_oncurve_angle(t, *points):
    if len(points) == 2:
        return 0
    onCurve = calcSeg(t, *points)
    d = calcDeriverate(*points) # 1st derivative
    dd = calcDeriverate(*d) # 2nd derivative
    dx, dy = calcSeg(t, *d)
    ddx, ddy = calcSeg(t, *dd)
    
    vectorAngle = calcAngle((0,0), (dx, dy))
     
    num = dx * ddy - ddx * dy
    dnom = math.pow(dx*dx + dy*dy, 3/2)
    if num == 0 or dnom == 0: 
        return 0
    return num / dnom, onCurve, vectorAngle

def getCurvatureVisLineForT(lengthMultiplier, angleModificator, t, *points):  
    data = calcCurvatureAtTA_oncurve_angle(t, *points)
    kappa, oncurve, vectorAngle = data
    refCurvaturePoint = (oncurve[0]+kappa*lengthMultiplier, oncurve[1])
    vectorAngle += angleModificator
    curvatureVis = rotatePoint(refCurvaturePoint, vectorAngle, oncurve)
    return oncurve, curvatureVis
    
points = (
        (130, 650),
        (410, 730),
        (570, 640),
        (750, 100)
    )

#points = tuple(reversed(points))

size(1000,1000)
#translate(1000,1000)
fill(None)
stroke(0)
strokeWidth(0.5)

drawBezier(*points)
d = calcDeriverate(*points)
#with savedState():
#    stroke(1,0,0)
#    drawBezier(*d)

steps = 1200
color1 = (1,0,0,.3)
color2 = (0,0,1,.7)
left = []
right = []
for i in range(steps):
    t = i/(steps-1)
    oncurve, curvatureVis = getCurvatureVisLineForT(100000, math.pi/2, t, *points)
    stroke(*interpolateSetSOfValues(color1, color2, t))
    line(oncurve, curvatureVis)
    fill(1)
    stroke(*interpolateSetSOfValues(color2, color1, t))
    # dp(curvatureVis,3)
    left.append(curvatureVis)
    oncurve, curvatureVis = getCurvatureVisLineForT(100000, -math.pi/2, t, *points)
    stroke(*interpolateSetSOfValues(color2, color1, t))
    line(oncurve, curvatureVis)
    stroke(*interpolateSetSOfValues(color1, color2, t))
    fill(1)
    # dp(curvatureVis,3)
    right.append(curvatureVis)
fill(None)
stroke(0)
polygon(*left, close=False)
polygon(*right, close=False)
stroke(0)
fill(1)
line(*points[:2])
line(*points[2:])
for p in list(points) + [(0,0)]:
    dp(p,5)