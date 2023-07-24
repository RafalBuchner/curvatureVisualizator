from random import random
import math
import inspect


"""
– ( geneticBezier() ) nowy, quasi genetyczny zapis funkcji beziera
    (aby byl zupelnie genetyczny, funkcjie binomial nalezy zastapic rownaniem: math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))

– ( bezier.drawDerivative(), derivativeBezier() ) dodalem motodę w klasie bezier umożliwiającą rysowanie pochodnej funkcji,
    co więcej: w funkcji umieściłem wzór genetyczny dla pochodnych od danej krzywej beziera

– ( bezier.zero ) DODAŁEM PUNKT ZEROWY do klasy bezier

– ( bezier.drawXextremum(), bezier.calculateExtremes() ) oddzieliłem rysowanie extremów od ich obliczania w dwie osobne metody klasy bezier
    (co więcej, oblicza cztery możliwe extrema: +x/-x/+y/-y)

– ( alignCurveToXaxis() realignCurve() ) stworzyłem funkcję rzutującą beziera do osi Xów

- ( bezier.drawBoundingBox() ) stworzyłem metodę rysującą Bounding Box dla klasy bezier

- ( movePointsFromList() ) stworzyłem funkcję zwracającą listę punktów o zmienionych współrzędnych o zadaną wartość

- ( drawTightBox() ) metoda klasy bezier, pozwalająca narysować BoundingBox dostosowany do kąta nachylenia krzywej względem osi X

– Poprawiłem rysowanie tangensa i normalnej dla wartości t równej zeru,oraz jednemu ( metoda bezier.drawTangentNormal() w klasie bezier )
"""
def dp(p, s=3):
    x, y = p
    r = s/2
    oval(x-r,y-r,s,s)
    
#nalezy: wyczyscic wszystkie calculateBezier i zastapic je geneticBezier

CANVAS = 1800

size(CANVAS, CANVAS) #DrawBot canvas

pascalTriangle = [      [1],           # n=0
                       [1,1],          # n=1
                      [1,2,1],         # n=2
                     [1,3,3,1],        # n=3
                    [1,4,6,4,1],       # n=4
                   [1,5,10,10,5,1],    # n=5
                  [1,6,15,20,15,6,1]]  # n=6

# Obliczanie tablicy punktów na bezierze dla zadanego beziera //sprawdź czym jest nazwa LUT!!!
def getLut(P1,P2,P3,P4):
    tablica = []
    for x in range(1,100):
        tablica.append( geneticBezierBetter(3,x/100,[P1.x,P2.x,P3.x,P4.x],[P1.y,P2.y,P3.y,P4.y]) )
    return tablica

def closest (LUT, pointOffCurve):
    minimalDist = 10000
    position = -1
    distance = 0
    for n in range(len(LUT)):
        distance = lenghtAB(pointOffCurve, LUT[n])

        if distance < minimalDist:
            minimalDist = distance
            position = n

    if position == -1:
        # print("f**k")
        return None

    return LUT[position]


def binomial(n,k):
    while n >= len(pascalTriangle):
        s = len(pascalTriangle)
        nextRow = []
        nextRow[0] = 1
        for i in range(s):
            prev = s-1
            nextRow[i]= pascalTriangle[prev][i-1] + pascalTriangle[prev][i]
        nextRow[s] = 1
        pascalTriangle.append(nextRow)
    return pascalTriangle[n][k]

def geneticBezier(n,t,w):

    summa = 0 #we wzorze wartosc i poczatkowa
    i = 0
    while i <= n:
        # zapis sumaryczny: dumian newtona o wartosci gornej n, dolnej i, pomnoz to z (1-t)do potegi n-1 razy t do potegi i
        summa += binomial(n,i) * (1-t)**(n-i) * t**i * w[i]
        i += 1
    return summa

##################### UUWWAAGGAA!!! LEPSZA WERSJA ZWRACAJĄCA PUNKT!!!
##################### UUWWAAGGAA!!! LEPSZA WERSJA ZWRACAJĄCA PUNKT!!!
def geneticBezierBetter(n,t,Wx,Wy): ##################### UUWWAAGGAA!!! LEPSZA WERSJA ZWRACAJĄCA PUNKT!!!

    summaY = 0 #we wzorze wartosc i poczatkowa
    summaX = 0 #we wzorze wartosc i poczatkowa
    i = 0
    while i <= n:
        # zapis sumaryczny: dumian newtona o wartosci gornej n, dolnej i, pomnoz to z (1-t)do potegi n-1 razy t do potegi i
        summaY += binomial(n,i) * (1-t)**(n-i) * t**i * Wy[i]
        summaX += binomial(n,i) * (1-t)**(n-i) * t**i * Wx[i]
        i += 1
    T = Point(summaX,summaY,"T")
    return T


def derivativeBezier(n,t,w):

    sum = 0 #we wzorze wartosc i poczatkowa
    i = 0
    k = n - 1
    while i <= k:
        # zapis sumaryczny: dumian newtona o wartosci gornej n, dolnej i, pomnoz to z (1-t)do potegi n-1 razy t do potegi i
        sum += binomial(k,i) * (1-t)**(k-i) * t**i * n*(w[i+1] - w[i])
        i += 1
    return sum

##################### UUWWAAGGAA!!! LEPSZA WERSJA ZWRACAJĄCA PUNKT!!!
##################### UUWWAAGGAA!!! LEPSZA WERSJA ZWRACAJĄCA PUNKT!!!
def derivativeBezierBetter(n,t,Wx,Wy): ##################### UUWWAAGGAA!!! LEPSZA WERSJA ZWRACAJĄCA PUNKT!!!

    summaX = 0 #we wzorze wartosc i poczatkowa
    summaY = 0 #we wzorze wartosc i poczatkowa
    i = 0
    k = n - 1
    while i <= k:
        # zapis sumaryczny: dumian newtona o wartosci gornej n, dolnej i, pomnoz to z (1-t)do potegi n-1 razy t do potegi i
        summaX += binomial(k,i) * (1-t)**(k-i) * t**i * n*(Wx[i+1] - Wx[i])
        summaY += binomial(k,i) * (1-t)**(k-i) * t**i * n*(Wy[i+1] - Wy[i])
        i += 1
    T = Point(summaX,summaY,"T")
    return T

def retrieve_name(var):
    #zwraca nazwe zmiennej w postaci str
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def angle( A, B ):
    """zmienna wskazująca kąt (w radianach) między odcinkiem, który przecina wskazane dwa punkty, a osią x"""
    xDiff = A.x - B.x
    yDiff = A.y - B.y
    if yDiff== 0 or xDiff== 0:
        tangens = 0
    else:
        tangens = yDiff / xDiff

    angle = math.atan( tangens )
    return angle

def lenghtAB(A,B):
    sqA = (B.x - A.x) **2
    sqB = (B.y - A.y) **2
    sqC = sqA + sqB
    if sqC > 0:
        lengthAB = sqrt(sqC)
        return lengthAB
    else:
        return 0

def rotatePoint( P,angle, originPointX, originPointY):
    """Rotates x/y around x_orig/y_orig by angle and returns result as [x,y]."""
    alfa = radians(angle)

    x = ( P.x - originPointX ) * cos( alfa ) - ( P.y - originPointY ) * sin( alfa ) + originPointX
    y = ( P.x - originPointX ) * sin( alfa ) + ( P.y - originPointY ) * cos( alfa ) + originPointY

    return x, y

def rotatePointsFromList(List,angle, originPoint):
    """Oblicza wspolrzedne dla punktu pochodnego od P przez transformacje obrotu o dany kąt angle względem punktu o współrzędnych originPointX, originPointY"""
    newList = []
    for n in range(len(List)):
        P = List[n]
        P = Point(rotatePoint(P, angle, originPoint.x,originPoint.y)[0],rotatePoint(P, angle, originPoint.x,originPoint.y)[1], "P"+str(n))
        newList.append(P)

    return newList

def inter(A,B,t):
    """PL:interpolacja pomiędzy punktami AB, przy stosunku t
    EN:interpolation between two points, with ratio t"""
    interAB = A*(1-t)+B*t
    return interAB

def CalculateBezier( x1,y1,  x2,y2,  x3,y3,  x4,y4,  t ):
    """PL:zwraca współrzędne punktu dla stosunku t (od 0 do 1) na podstawie wzoru na krzywą parametryczną trzeciego stopnia
    EN:returns coordinates for t ratio(from 0 to 1). Based on cubic bezier formula.
    """
    x = x1*(1-t)**3 + x2*3*t*(1-t)**2 + x3*3*t**2*(1-t) + x4*t**3
    y = y1*(1-t)**3 + y2*3*t*(1-t)**2 + y3*3*t**2*(1-t) + y4*t**3

    return x, y

def drawPointsFromList(listOfPoints,n,r,g,b,alfa):
    """
    PL: rysuje reprezentacje punktów zawartych w liście listOfPoints
    EN: draws representations of points grouped in listOfPoints
    """
    save()
    fill(r,g,b,alfa)
    if n == True:
        for n in range(len(listOfPoints)):
            name = listOfPoints[n].label
            x = listOfPoints[n].x
            y = listOfPoints[n].y
            text(name,(x+5,y+5))
            oval(listOfPoints[n].x-2, listOfPoints[n].y-2, 4, 4)
    else:
        for n in range(len(listOfPoints)):
            name = listOfPoints[n].label
            x = listOfPoints[n].x
            y = listOfPoints[n].y
            oval(listOfPoints[n].x-2, listOfPoints[n].y-2, 4, 4)

    restore()

def strokeAB(A,B):
    """
    PL: rysuje kreche z punktu A do B
    EN: draws stroke between points A and B
    """
    save()
    stroke(0,0,0)
    newPath()
    moveTo((A.x, A.y))
    lineTo((B.x, B.y))
    drawPath()
    restore()

def strokesFromList(listOfPoints,r,g,b,alfa,close):
    """PL: rysuje krechy punktów zawartych w liście listOfPoints
    EN: draws strokes between points in listOfPoints
    """

    save()
    stroke(r,g,b,alfa)
    fill(None)
    newPath()
    moveTo((listOfPoints[0].x, listOfPoints[0].y))
    for x in range(len(listOfPoints)):
        if x < len(listOfPoints)-1:


            lineTo((listOfPoints[x+1].x, listOfPoints[x+1].y))

        else:
            pass
    if close == True:
        closePath()
    else:
        pass
    drawPath()
    restore()

def movePointsFromList(listOfPoints,xJUMP,yJUMP):
    movedPoints = []
    for n in range(len(listOfPoints)):
        listOfPoints[n].x += xJUMP
        listOfPoints[n].y += yJUMP
        movedPoints.append(listOfPoints[n])
    return movedPoints

#MATH UTILITIES
def arcfn(n,t,Wx,Wy):
    d = derivativeBezierBetter(n,t,Wx,Wy)
    l = d.x*d.x + d.y*d.y
    return sqrt(l)

#OPERACJE NA FUNKCJACH
def splitCurve(oldCurve, t):
    """dzieli krzywą na dwie, w punkcie odpowiadajacym współczynnikowi t (t= 0 do 1)"""
    oldCurve.actual_t = t
    PA1 = oldCurve.P1
    PA2 = oldCurve.Q12
    PA3 = oldCurve.R1
    PA4 = oldCurve.D

    PB1 = oldCurve.D
    PB2 = oldCurve.R2
    PB3 = oldCurve.Q34
    PB4 = oldCurve.P4
    NewCurveA = Bezier(PA1,PA2,PA3,PA4,0)
    NewCurveB = Bezier(PB1,PB2,PB3,PB4,0)
    NewCurveA.drawBezier()
    NewCurveA.drawInterpolationPoints()
    NewCurveA.drawDeepInterpolationPoints()
    NewCurveA.drawAllControl()
    NewCurveA.drawInterpolationLines()
    NewCurveA.drawConvexHull()
    NewCurveA.drawXextremum()

    NewCurveB.drawBezier()
    NewCurveB.drawInterpolationPoints()
    NewCurveB.drawDeepInterpolationPoints()
    NewCurveB.drawAllControl()
    NewCurveB.drawInterpolationLines()
    NewCurveB.drawConvexHull()
    NewCurveB.drawXextremum()

def alignCurveToXaxis(curve):
    # works with cubic bezier curves
    # moves whole curve, so P1 has 0 coordinates for x and y
    # after usgin this aligment inside methods of bezier class, you should use realignCurve()
    alfa = -degrees(angle(curve.P1,curve.P4))
    xJUMP = -curve.P1.x
    yJUMP = -curve.P1.y
    listOfPoints = [curve.P1, curve.P2, curve.P3, curve.P4,]
    listOfRotatedPoints = movePointsFromList(listOfPoints,xJUMP,yJUMP)

    coo = rotatePointsFromList(listOfRotatedPoints,alfa,P1) # coordinates of aligned points

    curve = Bezier(coo[0], coo[1], coo[2], coo[3], 0)
    return curve

def realignCurve(curve, alfa, JUMPpoint):
    # repairs trash made by alignCurveToXaxis
    alfa = -alfa
    xJUMP = JUMPpoint.x
    yJUMP = JUMPpoint.y
    Plist = curve.Plist
    listOfRotatedPoints = movePointsFromList(Plist,xJUMP,yJUMP)
    coo = rotatePointsFromList(listOfRotatedPoints,alfa,P1) # coordinates of rotated points

    curve = Bezier(coo[0], coo[1], coo[2], coo[3], 0)

#KLASY
class Point(object):
    """PL: Tworzy obiekty punktów, których atrybutami są:
    współrzędna x,y
    nazwa
    EN: Creates point objects. Main attributes:
    coordinates x,y
    label
    """
    def __init__ (self,x,y,label):
        self.x = x
        self.y = y
        self.label = label
        pass
    #def moveTo(): #przemieszcza punkt w skazany
    #def moveBy(a, alfa): #rusza o iles jednostek w jakas strone, wyrazona w koncie

class Bezier(object):
    """PL: Tworząc obiekt, klasa potrzebuje:
    - cztery punkty kontrolne P1,P2,P3,P4
    - wartość t od 0 do 1, będąca stosunkiem,
    na którym opiera się interpolacja wszystkich
    punktów krzywej, poza punktami kontrolnymi

    EN: To create bezier objects you will need:
    - four "Point" objects (for control points):P1,P2,P3,P4
    - value for variable t, from 0 to 1. t is a ratio.
    Every interpolation-related calculations in this class will need t-ratio.
    """

    def __init__ (self, P1,P2,P3,P4,actual_t):

        self.name = retrieve_name(self)

        #POINT WITH COORDINATES: X = 0, Y = 0
        self.zero = Point(0,0,'ZERO')

        #ratio value
        self.actual_t = actual_t
        ###ZRÓB WARUNEK IF, W KTÓRYM: JEŚLI P1 ALBO P4 BEDZIE MIALO TE SAME WSPÓŁRZĘDNE, CO P3 ALBO P2, TO NIECH P1=P2, A P4=P3 (W TEN SPOSOB POWSTANIE OBLICZALNA LINIA CIAGLA), PO ELSE, NIECH BEDZIE TO CO JEST
        #control points
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4
        self.Plist = [self.P1,self.P2,self.P3,self.P4]

        #interpolation points based on de Casteljau's algorithm (coordinates are interpolations between control points and interpolation points)
        self.Q12 = Point(
                   inter(self.P1.x,self.P2.x,self.actual_t),
                   inter(self.P1.y,self.P2.y,self.actual_t),
                   'Q12')

        self.Q23 = Point(
                   inter(self.P2.x,self.P3.x,self.actual_t),
                   inter(self.P2.y,self.P3.y,self.actual_t),
                   'Q23')

        self.Q34 = Point(
                   inter(self.P3.x,self.P4.x,self.actual_t),
                   inter(self.P3.y,self.P4.y,self.actual_t),
                   'Q34')

        self.Qlist = [self.Q12, self.Q23, self.Q34]

        self.R1  = Point(
                   inter(self.Q12.x,self.Q23.x,self.actual_t),
                   inter(self.Q12.y,self.Q23.y,self.actual_t),
                   'R1')

        self.R2  = Point(
                   inter(self.Q23.x,self.Q34.x,self.actual_t),
                   inter(self.Q23.y,self.Q34.y,self.actual_t),
                   'R2')

        self.Rlist = [self.R1, self.R2]
        #Drawing Point

        self.D = Point(inter(self.R1.x,self.R2.x,self.actual_t),inter(self.R1.y,self.R2.y,self.actual_t),'D')
        self.derivativeD = Point(derivativeBezier(3, self.actual_t, [P1.x,P2.x,P3.x,P4.x]),derivativeBezier(3, self.actual_t, [P1.y,P2.y,P3.y,P4.y]), 'DD')
        self.Dlist = [self.D,self.derivativeD]

        # this is the same, but diffrent way of computing(without de Casteljau's algorithm):
        self.PointOfAcctual_t = Point(
                                CalculateBezier(self.P1.x,self.P1.y,self.P2.x,self.P2.y,self.P3.x,self.P3.y,self.P4.x,self.P4.y, self.actual_t)[0],
                                CalculateBezier(self.P1.x,self.P1.y,self.P2.x,self.P2.y,self.P3.x,self.P3.y,self.P4.x,self.P4.y, self.actual_t)[1],
                                "T")
        self.extreme = 0

    def PointOnCurveWithRatio(self, t, strName):
        x = geneticBezier(3, t, [self.P1.x,self.P2.x,self.P3.x,self.P4.x])
        y = geneticBezier(3, t, [self.P1.y,self.P2.y,self.P3.y,self.P4.y])
        PointOnCurve = Point(x,y,strName)
        return PointOnCurve

    def scaleOfCovexHull(self):
        """zwraca stosunek (wyrażony jako float) dlugosci covexhull do średniej kwadratowej wymiarów Canvas DrawBota, pomnożoną przez wartość 0.0004"""
        lengthOfHull = lenghtAB(P1,P2)+lenghtAB(P2,P3)+lenghtAB(P3,P4)
        DrawBotWidth = width()
        DrawBotHeight = height()
        rootMeanSquare = sqrt(DrawBotWidth**2 + DrawBotHeight**2)/2
        scale = rootMeanSquare / lengthOfHull * 0.004

        return scale

    def drawBezier(self,r,g,b):

        stepsOFt = self.scaleOfCovexHull() * 0.25
        t = 0
        save()
        stroke(None)
        while t <= 1:
            x = geneticBezier(3, t, [self.P1.x,self.P2.x,self.P3.x,self.P4.x])
            y = geneticBezier(3, t, [self.P1.y,self.P2.y,self.P3.y,self.P4.y])
            fill(r,g,b,0.5)
            dp((x,y))
            t = t+stepsOFt
        restore()
        t = 0

    def drawDerivative(self):

        stepsOFt = self.scaleOfCovexHull() * 0.25
        t = 0
        save()
        while t <= 1:
            x = derivativeBezier(3, t, [self.P1.x,self.P2.x,self.P3.x,self.P4.x])
            y = derivativeBezier(3, t, [self.P1.y,self.P2.y,self.P3.y,self.P4.y])

            fill(1,0,0.5,1)
            oval(x-0.5, y-0.5, 1, 1) #draws point on the screen

            t = t+stepsOFt
        restore()
        t = 0

    def drawTangentNormal(self):
        """PL:Rysuje tangens oraz normalną krzywej w punkcie przy zadanej wartości stosunku t
        EN:Draws tangent and normal for point calculated with current ratio t"""
        x = self.PointOfAcctual_t.x
        y = self.PointOfAcctual_t.y

        if self.D.x == self.P4.x and self.D.y == self.P4.y:
            #operation, that calculates tangent for t = 1. Without it, our tangent will be paraller to Xaxis
            yTanDistance = 35 * sin(angle(self.P4,self.P3))
            xTanDistance = 35 * cos(angle(self.P4,self.P3))
            xTan = xTanDistance + self.D.x
            yTan = yTanDistance + self.D.y
            p_t_is_zero = Point(xTan,yTan,"temp")
            xTan = rotatePoint(p_t_is_zero,180,self.P4.x,self.P4.y)[0]
            yTan = rotatePoint(p_t_is_zero,180,self.P4.x,self.P4.y)[1]
        else:
            # operation, that calculates tangent fo t, that: 0 <= t < 1
            yTanDistance = 35 * sin(angle(self.D,self.R2))
            xTanDistance = 35 * cos(angle(self.D,self.R2))
            xTan = xTanDistance + self.D.x
            yTan = yTanDistance + self.D.y

        self.tan = Point(xTan,yTan,"Tan")
        self.Normal = Point(rotatePoint(self.tan, 90, self.D.x,self.D.y)[0],rotatePoint(self.tan, 90, self.D.x,self.D.y)[1],"Normal")

        save()
        stroke(1,0,0)
        strokeAB(self.D,self.Normal)
        strokeAB(self.D,self.tan)

        fill(0,0,5)
        oval(self.Normal.x-2, self.Normal.y-2, 4, 4)
        fill(1,1,0,1.0)
        oval(self.tan.x-2, self.tan.y-2, 4, 4)
        restore()

    def calculateExtremes(self):

        stepsOFt = self.scaleOfCovexHull() * 0.25
        everyPointOnCurve = []


        t = 0
        while t <= 1:
            x = CalculateBezier(self.P1.x,self.P1.y,self.P2.x,self.P2.y,self.P3.x,self.P3.y,self.P4.x,self.P4.y, t)[0] #difference between PointOfActual_t is: drawBezier uses its own, proggresive t ratio
            y = CalculateBezier(self.P1.x,self.P1.y,self.P2.x,self.P2.y,self.P3.x,self.P3.y,self.P4.x,self.P4.y, t)[1]
            PointOnCurve = [x,y]
            everyPointOnCurve.append(PointOnCurve)
            t = t+stepsOFt


        everyYOnCurve = []
        everyXOnCurve = []

        for n in range(len(everyPointOnCurve)):
            everyXOnCurve.append(everyPointOnCurve[n][0])
            everyYOnCurve.append(everyPointOnCurve[n][1])

        extremeXplus = max(everyXOnCurve)
        extremeYplus = max(everyYOnCurve)
        extremeXmin = min(everyXOnCurve)
        extremeYmin = min(everyYOnCurve)
        XforExtremeYplus = 0
        YforExtremeXplus = 0
        XforExtremeYmin = 0
        YforExtremeXmin = 0
        for n in range(len(everyPointOnCurve)):
            #plus
            if everyPointOnCurve[n][0] == extremeXplus:
                YforExtremeXplus = everyPointOnCurve[n][1]
            elif everyPointOnCurve[n][1] == extremeYplus:
                XforExtremeYplus = everyPointOnCurve[n][0]
            #minus
            elif everyPointOnCurve[n][0] == extremeXmin:
                YforExtremeXmin = everyPointOnCurve[n][1]
            elif everyPointOnCurve[n][1] == extremeYmin:
                XforExtremeYmin = everyPointOnCurve[n][0]

        self.ExtremeXaxisPLUS = Point(extremeXplus,YforExtremeXplus,'ExXplus')
        self.ExtremeYaxisPLUS = Point(XforExtremeYplus,extremeYplus,'ExYplus')
        self.ExtremeXaxisMIN = Point(extremeXmin,YforExtremeXmin,'ExXmin')
        self.ExtremeYaxisMIN = Point(XforExtremeYmin,extremeYmin,'ExYmin')
        return self.ExtremeXaxisPLUS, self.ExtremeYaxisPLUS, self.ExtremeXaxisMIN , self.ExtremeYaxisMIN

    def calculateBoundingBox(self):
        self.calculateExtremes()
        A_BB = Point(self.ExtremeXaxisMIN.x,self.ExtremeYaxisMIN.y,"A_BB")
        B_BB = Point(self.ExtremeXaxisMIN.x,self.ExtremeYaxisPLUS.y,"B_BB")
        C_BB = Point(self.ExtremeXaxisPLUS.x,self.ExtremeYaxisPLUS.y,"C_BB")
        D_BB = Point(self.ExtremeXaxisPLUS.x,self.ExtremeYaxisMIN.y,"D_BB")
        BB_Points = [A_BB, B_BB, C_BB, D_BB]
        return BB_Points

    def calculateInflection(self):
        stepsOFt = self.scaleOfCovexHull() * 0.25

        # dla ułatwienia obliczeń rzutujemy krzywą na oś X (w rezultacie wartości punktów początkowych i końcowych wyniosą zero dla przynajmniej jednej osi)
        xJUMP = self.P1.x
        yJUMP = self.P1.y
        JUMPpoint = Point(xJUMP,yJUMP,'JUMP')
        alfa = degrees(angle(self.P1,self.P4))


        # print( yJUMP)  ###test
        aligned = alignCurveToXaxis(self) ###TO PRZEKRĘCA NA STAŁĘ!!!!
        # print( yJUMP, self.P1.y, JUMPpoint.y  )###test

        aP1 = aligned.P1
        aP2 = aligned.P2
        aP3 = aligned.P3
        aP4 = aligned.P4

        # szukamy wartosći t, dla której kurwatura funkcji bezier wyniesie zero
        # wzor wartosci krzywizny (curvature) zerowej: C = Bezier'(t) * Bezier''(t) - Bezier'(t) * Bezier''(t)
        a = aP3.x * aP2.y
        b = aP4.x * aP2.y
        c = aP2.x * aP3.y
        d = aP4.x * aP3.y

        x = 18*( -3*a + 2*b + 3*c - d )
        y = 18*( 3*a - b - 3*c )
        z = 18*( c - a )

        D = y**2 - 4*x*z ### discriminant/ wyróżnik równania kwadratowego

        if D >= 0 and x != 0:
            """jeśli  wyróżnik jest l. naturalną, a mianownik nie równa się zeru, to: oblicz równanie kwadratowe
            (popatrz na https://pomax.github.io/bezierinfo/#inflections),
            wyniki w takim równaniu są dwa: jeśli jeden z nich znajduje się w przedziale 0<t<1,
            to jest to ratio t, dla którego wartosc funkcji beziera bedzie obliczala punkt infekcyjny"""

            t1 = (-y + sqrt(D)) / (2*x) #
            t2 = (-y - sqrt(D)) / (2*x) #



            if t1 <= 1 and 0 <= t1:
                aligned = realignCurve(self, alfa, JUMPpoint)
                #InfPoint = self.PointOnCurveWithRatio(t1,"Inf")
                return t1

            elif t2 <= 1 and 0 <= t2:
                aligned = realignCurve(self, alfa, JUMPpoint)
                #InfPoint = self.PointOnCurveWithRatio(t2,"Inf")
                return t2

            return #InfPoint
        else:
            aligned = realignCurve(self, alfa, JUMPpoint)

    def calculateTightBox(self):
        """metoda klasy bezier, pozwalająca narysować BoundingBox dostosowany do kąta nachylenia krzywej względem osi X

        1)najpierw zapamietuje wspolrzedne, ktore sa potrzebne dla funkcji alignCurveToXaxis():
            1)wartosc przesuniecia calej krzywej do poczatku ukladu wpolrzednych(xJUMP, yJUMP)
            2) kąt, dzięki któremu krzywa zostaje zrzutowana do osi X,
        2)Potem orginalną krzywą rzutuje do osi X
        3)Zrzutowaną krzywą do osi X zamyka w BoindingBoxie
        4)Za pomocą wcześniej pobranych danych (xJUMP,yJUMP oraz alfa) przesówa boundingboxa, dostosowując go do samej krzywej."""

        xJUMP = self.P1.x
        yJUMP = self.P1.y
        JUMPpoint = Point(xJUMP,yJUMP,'JUMP')

        alfa = degrees(angle(self.P1,self.P4))

        aligned = alignCurveToXaxis(self) #1
        aligned.calculateExtremes()

        #aligned boudingbox points
        BB_Points = aligned.calculateBoundingBox()

        movedBBpoints = movePointsFromList(BB_Points,xJUMP,yJUMP)
        movedAndRotatedBBpoints = rotatePointsFromList(movedBBpoints,alfa,JUMPpoint)

        return movedAndRotatedBBpoints

    def calculateLength(self):#### UWAGA
        #n = 24
        #weight:
        cValues = [0.1279381953467521569740561652246953718517,0.1279381953467521569740561652246953718517,0.1258374563468282961213753825111836887264,0.1258374563468282961213753825111836887264,0.1216704729278033912044631534762624256070,0.1216704729278033912044631534762624256070,0.1155056680537256013533444839067835598622,0.1155056680537256013533444839067835598622,0.1074442701159656347825773424466062227946,0.1074442701159656347825773424466062227946,0.0976186521041138882698806644642471544279,0.0976186521041138882698806644642471544279,0.0861901615319532759171852029837426671850,0.0861901615319532759171852029837426671850,0.0733464814110803057340336152531165181193,0.0733464814110803057340336152531165181193,0.0592985849154367807463677585001085845412,0.0592985849154367807463677585001085845412,0.0442774388174198061686027482113382288593,0.0442774388174198061686027482113382288593,0.0285313886289336631813078159518782864491,0.0285313886289336631813078159518782864491,0.0123412297999871995468056670700372915759,0.0123412297999871995468056670700372915759]
        #abscissa:
        tValues = [-0.0640568928626056260850430826247450385909,0.0640568928626056260850430826247450385909,-0.1911188674736163091586398207570696318404,0.1911188674736163091586398207570696318404,-0.3150426796961633743867932913198102407864,0.3150426796961633743867932913198102407864,-0.4337935076260451384870842319133497124524,0.4337935076260451384870842319133497124524,-0.5454214713888395356583756172183723700107,0.5454214713888395356583756172183723700107,-0.6480936519369755692524957869107476266696,0.6480936519369755692524957869107476266696,-0.7401241915785543642438281030999784255232,0.7401241915785543642438281030999784255232,-0.8200019859739029219539498726697452080761,0.8200019859739029219539498726697452080761,-0.8864155270044010342131543419821967550873,0.8864155270044010342131543419821967550873,-0.9382745520027327585236490017087214496548,0.9382745520027327585236490017087214496548,-0.9747285559713094981983919930081690617411,0.9747285559713094981983919930081690617411,-0.9951872199970213601799974097007368118745,0.9951872199970213601799974097007368118745]

        ###### def arcfn(n,t,Wx,Wy):
        ######     d = derivativeBezierBetter(n,t,Wx,Wy)
        ######     l = d.x*d.x + d.y*d.y
        ######     return sqrt(l)

        Wx = [self.P1.x,self.P2.x,self.P3.x,self.P4.x]
        Wy = [self.P1.y,self.P2.y,self.P3.y,self.P4.y]

        t = 0
        summa = 0
        z = 0.5

        for i in range(len(cValues)):

            t = z * tValues[i] + z
            summa += cValues[i] * arcfn(3,t,Wx,Wy)

        lenght = z * summa
        # print(lenght) ### test
        return lenght

    ################################################## TESTE
    def intervals(self, i):
        lengthOfCurve = self.calculateLength()
        intervalDistance = lengthOfCurve / i

    def drawRegularDistance(self):#### DO POPRAWKI
        #n = 100
        #weight:
        cValues = [0.0312554234538634,0.0312554234538634,0.0312248842548494,0.0312248842548494,0.0311638356962099,0.0311638356962099,0.0310723374275665,0.0310723374275665,0.0309504788504910,0.0309504788504910,0.0307983790311526,0.0307983790311526,0.0306161865839804,0.0306161865839804,0.0304040795264548,0.0304040795264548,0.0301622651051691,0.0301622651051691,0.0298909795933328,0.0298909795933328,0.0295904880599126,0.0295904880599126,0.0292610841106383,0.0292610841106383,0.0289030896011252,0.0289030896011252,0.0285168543223951,0.0285168543223951,0.0281027556591012,0.0281027556591012,0.0276611982207924,0.0276611982207924,0.0271926134465769,0.0271926134465769,0.0266974591835710,0.0266974591835710,0.0261762192395457,0.0261762192395457,0.0256294029102081,0.0256294029102081,0.0250575444815796,0.0250575444815796,0.0244612027079571,0.0244612027079571,0.0238409602659682,0.0238409602659682,0.0231974231852541,0.0231974231852541,0.0225312202563362,0.0225312202563362,0.0218430024162474,0.0218430024162474,0.0211334421125276,0.0211334421125276,0.0204032326462094,0.0204032326462094,0.0196530874944353,0.0196530874944353,0.0188837396133749,0.0188837396133749,0.0180959407221281,0.0180959407221281,0.0172904605683236,0.0172904605683236,0.0164680861761452,0.0164680861761452,0.0156296210775460,0.0156296210775460,0.0147758845274413,0.0147758845274413,0.0139077107037188,0.0139077107037188,0.0130259478929715,0.0130259478929715,0.0121314576629795,0.0121314576629795,0.0112251140231860,0.0112251140231860,0.0103078025748690,0.0103078025748690,0.0093804196536945,0.0093804196536945,0.0084438714696690,0.0084438714696690,0.0074990732554647,0.0074990732554647,0.0065469484508453,0.0065469484508453,0.0055884280038655,0.0055884280038655,0.0046244500634221,0.0046244500634221,0.0036559612013264,0.0036559612013264,0.0026839253715535,0.0026839253715535,0.0017093926535181,0.0017093926535181,0.0007346344905057,0.0007346344905057]
        #abscissa:
        tValues = [-0.0156289844215431,0.0156289844215431,-0.0468716824215920,0.0468716824215920,-0.0780685828134367,0.0780685828134367,-0.1091892035800611,0.1091892035800611,-0.1402031372361140,0.1402031372361140,-0.1710800805386033,0.1710800805386033,-0.2017898640957360,0.2017898640957360,-0.2323024818449740,0.2323024818449740,-0.2625881203715035,0.2625881203715035,-0.2926171880384720,0.2926171880384720,-0.3223603439005292,0.3223603439005292,-0.3517885263724217,0.3517885263724217,-0.3808729816246300,0.3808729816246300,-0.4095852916783015,0.4095852916783015,-0.4378974021720315,0.4378974021720315,-0.4657816497733580,0.4657816497733580,-0.4932107892081909,0.4932107892081909,-0.5201580198817631,0.5201580198817631,-0.5465970120650942,0.5465970120650942,-0.5725019326213812,0.5725019326213812,-0.5978474702471787,0.5978474702471787,-0.6226088602037078,0.6226088602037078,-0.6467619085141293,0.6467619085141293,-0.6702830156031410,0.6702830156031410,-0.6931491993558020,0.6931491993558020,-0.7153381175730564,0.7153381175730564,-0.736828089802021,0.736828089802021,-0.7575981185197072,0.7575981185197072,-0.7776279096494955,0.7776279096494955,-0.7968978923903145,0.7968978923903145,-0.8153892383391763,0.8153892383391763,-0.8330838798884008,0.8330838798884008,-0.8499645278795913,0.8499645278795913,-0.8660146884971646,0.8660146884971646,-0.8812186793850184,0.8812186793850184,-0.8955616449707270,0.8955616449707270,-0.9090295709825297,0.9090295709825297,-0.9216092981453340,0.9216092981453340,-0.9332885350430795,0.9332885350430795,-0.944055870136256,0.944055870136256,-0.9539007829254917,0.9539007829254917,-0.9628136542558155,0.9628136542558155,-0.9707857757637063,0.9707857757637063,-0.9778093584869183,0.9778093584869183,-0.9838775407060570,0.9838775407060570,-0.9889843952429917,0.9889843952429917,-0.9931249370374435,0.9931249370374435,-0.9962951347331251,0.9962951347331251,-0.9984919506395958,0.9984919506395958,-0.9997137267734412,0.9997137267734412]

        ###### def arcfn(n,t,Wx,Wy):
        ######     d = derivativeBezierBetter(n,t,Wx,Wy)
        ######     l = d.x*d.x + d.y*d.y
        ######     return sqrt(l)

        Wx = [self.P1.x,self.P2.x,self.P3.x,self.P4.x]
        Wy = [self.P1.y,self.P2.y,self.P3.y,self.P4.y]

        tList = []
        t = 0
        summa = 0
        z = 0.5

        for i in range(len(cValues)):

            t = z * tValues[i] + z
            summa += cValues[i] * arcfn(3,t,Wx,Wy)
            tList.append(t)

        lenght = z * summa

        # print(tList) ### test
        for i in range(len(tList)):
            self.drawT(tList[i])


    def drawBoundingBox(self):
        strokesFromList(self.calculateBoundingBox(),0,1,0.2,1,True)

    def drawTightBox(self):
        strokesFromList(self.calculateTightBox(),0,1,0.2,1,True)

    def drawXextremum(self):
        extremes = list(self.calculateExtremes())

        drawPointsFromList(extremes,0,0.9,0.1,0.6,1.0)

    def drawAllControl(self):

        drawPointsFromList(self.Plist,1,0.7,0.7,0.7,1.0)

    def drawInterpolationPoints(self):

        drawPointsFromList(self.Qlist,1,0.1,0.7,0.7,1.0)

    def drawDeepInterpolationPoints(self):

        drawPointsFromList(self.Rlist,1,0.7,0.7,0.7,1.0)
        drawPointsFromList(self.Dlist,1,1,0,0,1.0)

    def drawInterpolationLines(self):

        strokesFromList(self.Rlist,1,0,0.5,1,False)
        strokesFromList(self.Qlist,0,0,0.5,1,False)
        pass

    def drawConvexHull(self):

        strokesFromList(self.Plist,0.9,0.9,0.9,1,False)

    def drawInflection(self):

        InfT = self.calculateInflection()
        InfPoint = self.PointOnCurveWithRatio(InfT,"Inf")
        if InfPoint == None:
            pass
        else:
            # print(InfT) # test
            save()
            fill(None)
            strokeWidth(3)
            stroke(0,0,0)
            oval(InfPoint.x-7, InfPoint.y-7, 14, 14)
            stroke(None)
            fill(0,0,0,1)
            oval(InfPoint.x-2, InfPoint.y-2, 4, 4)
            restore()

    def drawT(self, t):
        Point = self.PointOnCurveWithRatio(t, "T")
        save()
        fill(1,0,0,1)
        oval(Point.x-2, Point.y-2, 4, 4)
        restore()


strokeWidth(1)
#COMMANDS:
P1 = Point(300,300,'P1')
P2 = Point(350,500,'P2')
P3 = Point(600,450,'P3')
P4 = Point(600,300,'P4')

#
#P1 = Point(100,500,'P1')
#P2 = Point(35,300,'P2')
#P3 = Point(449,225,'P3')
#P4 = Point(335,60,'P4')
#
# P1 = Point(0,0,'P1')
# P2 = Point(0,225,'P2')
# P3 = Point(336,225,'P3')
# P4 = Point(336,0,'P4')
#
# P1 = Point(25,0,'P1')
# P2 = Point(10,450,'P2')
# P3 = Point(300,100,'P3')
# P4 = Point(120,10,'P4')
#
# P1 = Point(0,0,'P1')
# P2 = Point(0,0,'P2')
# P3 = Point(500,500,'P3')
# P4 = Point(500,500,'P4')
curve = Bezier(P1,P2,P3,P4,0.5)


#Placement of the curve
curve.calculateExtremes()
curveWidth = curve.ExtremeXaxisPLUS.x - curve.ExtremeXaxisMIN.x
curveHeight = curve.ExtremeYaxisPLUS.y - curve.ExtremeYaxisMIN.y
#translate(CANVAS/2 - curveWidth/2,CANVAS/2 - curveHeight/2)

curve.drawBezier(0.3,0,0.9)

# curve.drawInflection()
# curve.drawT(0.5)
curve.drawConvexHull()
#curve.drawBezier(0.3,0,0.9)
curve.calculateLength()
# curve.drawRegularDistance()


# curve.drawBoundingBox()
# curve.drawDerivative()
# curve.drawInterpolationPoints()
# curve.drawDeepInterpolationPoints()
# curve.drawAllControl()
# curve.drawInterpolationLines()
# curve.drawXextremum()
# curve.drawTangentNormal()
# curve.drawTightBox()

# align = alignCurveToXaxis(curve)
# align.drawBezier(0.3,0,0.9)
# align.drawBoundingBox()
# align.drawConvexHull()
# align.drawInflection()


#axis
# save()
# stroke(0,0,0,0.1)
# newPath()
# moveTo((-CANVAS, curve.zero.y))
# lineTo((CANVAS, curve.zero.y))
# drawPath()
# newPath()
# moveTo((curve.zero.y, CANVAS))
# lineTo((curve.zero.y, -CANVAS))
# drawPath()
# restore()

#testClosest = Point(336/2,0,'TEST')
#oval(testClosest.x-2, testClosest.y-2, 4, 4)

#LUTSHIT = getLut(P1,P2,P3,P4)

#PUNKT_close = closest(LUTSHIT,testClosest)
#oval(PUNKT_close.x-2, PUNKT_close.y-2, 4, 4)




#axis
stroke(0,0,0,0.1)
line((-CANVAS, curve.zero.y),(CANVAS, curve.zero.y))
line((curve.zero.y, CANVAS),(curve.zero.y, -CANVAS))

