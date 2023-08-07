import math


def derivativeCBezier(t, *pointList):
    """calculates derivative values for given control points and current t-factor"""
    ### http://www.idav.ucdavis.edu/education/CAGDNotes/Quadratic-Bezier-Curves.pdf ### Quadratic
    p1x, p1y = pointList[0]
    p2x, p2y = pointList[1]
    p3x, p3y = pointList[2]
    p4x, p4y = pointList[3]

    summaX = (
        -3 * p1x * (1 - t) ** 2
        + p2x * (3 * (1 - t) ** 2 - 6 * (1 - t) * t)
        + p3x * (6 * (1 - t) * t - 3 * t**2)
        + 3 * p4x * t**2
    )
    summaY = (
        -3 * p1y * (1 - t) ** 2
        + p2y * (3 * (1 - t) ** 2 - 6 * (1 - t) * t)
        + p3y * (6 * (1 - t) * t - 3 * t**2)
        + 3 * p4y * t**2
    )

    return summaX, summaY


def derivativeQBezier(t, *pointList):
    def derivativeQuadraticBezier(t, *pointList):
        """calculates derivative values for given control points and current t-factor"""
        p1x, p1y = pointList[0]
        p2x, p2y = pointList[1]
        p3x, p3y = pointList[2]

        summaY = 2 * (1 - t) * (p2y - p1y) + 2 * t * (p3y - p2y)
        summaX = 2 * (1 - t) * (p2x - p1x) + 2 * t * (p3x - p2x)

        return summaX, summaY

    assert len(pointList) == 4 and isinstance(t, float)
    p1 = pointList[0]
    h1 = pointList[1]
    h2 = pointList[2]
    p2 = pointList[3]
    c = calcLine(0.5, h1, h2)
    if t <= 0.5:
        t_segment = t * 2
        return derivativeQuadraticBezier(t_segment, p1, h1, c)
    else:
        t_segment = (t - 0.5) * 2
        return derivativeQuadraticBezier(t_segment, p2, h2, c)


def calcQbezier(t, *pointList):
    """returns coordinates for factor called "t"(from 0 to 1). Based on Quadratic Bezier formula."""

    def calcQuadraticBezier(t, *pointList):
        assert len(pointList) == 3 and isinstance(t, float)
        p1x, p1y = pointList[0]
        p2x, p2y = pointList[1]
        p3x, p3y = pointList[2]
        x = (1 - t) ** 2 * p1x + 2 * (1 - t) * t * p2x + t**2 * p3x
        y = (1 - t) ** 2 * p1y + 2 * (1 - t) * t * p2y + t**2 * p3y
        return x, y

    assert len(pointList) == 4 and isinstance(t, float)
    p1 = pointList[0]
    h1 = pointList[1]
    h2 = pointList[2]
    p2 = pointList[3]
    c = calcLine(0.5, h1, h2)
    if t <= 0.5:
        t_segment = t * 2
        return calcQuadraticBezier(t_segment, p1, h1, c)
    else:
        t_segment = (t - 0.5) * 2
        return calcQuadraticBezier(t_segment, p2, h2, c)


def calcCBezier(t, *pointList):
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


def calculateTangentAngle(segType, t, *points):
    """Calculates tangent angle for curve's/lines's current t-factor"""
    if len(points) == 4 and segType != "qcurve":
        xT, yT = calcCBezier(t, *points)
        xB, yB = derivativeCBezier(t, *points)
    if len(points) == 4 and segType == "qcurve":
        xT, yT = calcQbezier(t, *points)
        xB, yB = derivativeQBezier(t, *points)
    if len(points) == 2:
        xB, yB = points[-1]

    return angle((0, 0), (xB, yB))


def angle(A, B):
    """returns angle between line AB and axis x"""
    ax, ay = A
    bx, by = B
    xDiff = ax - bx
    yDiff = ay - by
    if yDiff == 0 or xDiff == 0 and ay == by:
        angle = 0
    elif yDiff == 0 or xDiff == 0 and ax == bx:
        angle = 90
    else:
        tangens = yDiff / xDiff
        angle = math.degrees(math.atan(tangens))

    return angle


# import math

# def setup():
#     global q, c
#     q = Bezier(this, 60, 55, 125, 160, 365, 165)
#     c = Bezier(this, 385, 165, 645, 165, 645, 70, 750, 165)
#     if (this.parameters.omni):
#         setSlider('.slide-control', 'position', 0)
#     setMovable(q.points + c.points)

# def draw():
#     clear()
#     for curve in [q, c]:
#         curve.drawSkeleton()
#         curve.drawCurve()
#         drawCurvature(curve)
#         curve.drawPoints()

#     if (this.parameters.omni):
#         t = this.position
#         curve = q
#         if (t > 1):
#             t -= 1
#             curve = c
#         drawIncidentCircle(curve, t)

# def drawCurvature(curve):
#     for s in range(256):
#         t = s / 255
#         p = curve.get(t)
#         n = curve.normal(t)
#         k = computeCurvature(curve, t) * 10000
#         ox = k * n.x
#         oy = k * n.y
#         setStroke(f'rgba(255,127,{s},0.6)')
#         line(p.x, p.y, p.x + ox, p.y + oy)
#         if (this.parameters.omni):
#             setStroke(f'rgba({s},127,255,0.6)')
#             line(p.x, p.y, p.x - ox, p.y - oy)

# def computeCurvature(curve, t):
#     d = curve.derivative(t)
#     dd = curve.dderivative(t)
#     num = d.x * dd.y - d.y * dd.x
#     qdsum = d.x * d.x + d.y * d.y
#     dnm = qdsum ** (3/2)
#     if (num == 0 or dnm == 0):
#         return 0
#     return num / dnm

def computeCurvature(t, *pointList):

    d = derivativeCBezier(t, *pointList) 
    dd = curve.dderivative(t) # second deriverate
    num = d.x * dd.y - d.y * dd.x
    qdsum = d.x * d.x + d.y * d.y
    dnom = qdsum ** (3/2)
    if (num == 0 or dnom == 0):
        return 0
    return num / dnom
