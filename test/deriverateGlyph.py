from deriverateLib import interpolateTwoSetsOfValues, getCurvatureVisLineForT
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
    



    
points = (
        (112, 270),
        (112, 446),
        #(670, 366),
        (250, 446)
    )



#points = tuple(reversed(points))

size(1000,1000)
#translate(1000,1000)
fill(None)
stroke(0)
strokeWidth(0.5)

drawBezier(*points)



steps = 200
color1 = (1,0,0,1)
color1 = (.1,.1,.5,.2)
color2 = (.1,.1,.5,.2)

color1 = (1,0,0,.5)
color2 = (1,1,1,1)
left = []
right = []

lengthMultiplier = 20000

for i in range(steps):
    nextIdx = i + 1
    
    t = i/(steps-1)
    
    angleModificator1 = -math.pi/2
    oncurve1, curvatureVis1 = getCurvatureVisLineForT(lengthMultiplier, angleModificator1, t, *points)
    left.append(curvatureVis1)
    
    angleModificator2 = math.pi/2
    oncurve2, curvatureVis2 = getCurvatureVisLineForT(lengthMultiplier, angleModificator2, t, *points)
    right.append(curvatureVis2)
    
    if nextIdx < steps:
        next_t = nextIdx/(steps-1)
        next_oncurve1, next_curvatureVis1 = getCurvatureVisLineForT(lengthMultiplier, angleModificator1, next_t, *points)
        next_oncurve2, next_curvatureVis2 = getCurvatureVisLineForT(lengthMultiplier, angleModificator2, next_t, *points)
        
    stroke(None)
    fill(*interpolateTwoSetsOfValues(t, color1, color2))
    polygon(oncurve1, curvatureVis1, next_curvatureVis1, next_oncurve1)
    
    fill(*interpolateTwoSetsOfValues(t, color2, color1))
    polygon(oncurve2, curvatureVis2, next_curvatureVis2, next_oncurve2)
    

    
    
    
fill(None)

stroke(0)
strokeWidth(0.2)
stroke(*color1[:-1])
polygon(*left, close=False)
stroke(*color1[:-1])
polygon(*right, close=False)
stroke(0)
fill(1)


line(*points[:2])

line(*points[-2:])

stroke(0)
for p in list(points) + [(0,0)]:
    dp(p,5)