import drawBot as bot
from fontTools.pens.basePen import AbstractPen
from deriverateLib import interpolateTwoSetsOfValues, getCurvatureVisLineForT, drawCurvatureVisForCurve_drawBot, drawCurvatureVisForCurveWith2ColorGradient_drawBot
import math, pprint



def dp(p, s=5):
    x, y = p
    r = s/2
    bot.oval(x-r,y-r,s,s)

def dps(*ps):
    for i,p in enumerate(ps):
        dp(p)

# # oncurve1, curvatureVis1 = getCurvatureVisLineForT(
# lengthMultiplier, 
# angleModificator1, 
# t, *points)

class CurvaturePen(AbstractPen):
    lastPoint = None

    def __init__(self, steps=200, lengthMultiplier=2000, clockwise=True, counterclockwise=True, colorPalette=((1,.8,0,.5),)):
        self.steps = steps
        self.lengthMultiplier = lengthMultiplier
        self.clockwise = clockwise
        self.counterclockwise = counterclockwise
        self.setcolorPalette(colorPalette)

    def setcolorPalette(self, colorPalette):
        if len(colorPalette) == 1:
            self.drawingMethod = drawCurvatureVisForCurve_drawBot
            self.colorPalette = colorPalette[0]
        elif len(colorPalette) == 2:
            self.drawingMethod = drawCurvatureVisForCurveWith2ColorGradient_drawBot
            self.colorPalette = colorPalette

        

    def moveTo(self, pt):
        dp(pt)

        self.lastPoint = pt

    def lineTo(self, pt):
        dp(pt)

        self.lastPoint = pt

    def qCurveTo(self, *points):
        # dividing segments into chunks of 3 points
        appendCount = 0
        prevPoint = self.lastPoint
        segs = []
        seg = [prevPoint]
        for idx, point in enumerate(points):

            if idx == 0 or idx == len(points)-1:
                appendCount += 1
                if idx == len(points)-1:
                    seg.append(prevPoint)
                    seg.append(point)
                    segs.append(seg)
                prevPoint = point
                continue

            midPoint = interpolateTwoSetsOfValues(.5, prevPoint, point)
            seg.append(prevPoint)
            appendCount += 1
            seg.append(midPoint)
            segs.append(seg)
            seg = [midPoint]
            appendCount += 1
            prevPoint = point


        for seg in segs:
            a, b, c = seg
            if self.clockwise:
                self.drawingMethod(self.colorPalette, self.lengthMultiplier, math.pi/2, self.steps, a, b, c)
            if self.counterclockwise:
                self.drawingMethod(self.colorPalette, self.lengthMultiplier, -math.pi/2, self.steps, a, b, c)
            with bot.savedState():
                bot.stroke(0)
                bot.line(a, b)
                bot.line(b, c)
            dps(*seg)
        self.lastPoint = points[-1]

    def curveTo(self, *points):
        a = self.lastPoint
        b, c, d = points
        if self.clockwise:
            self.drawingMethod(self.colorPalette, self.lengthMultiplier, math.pi/2, self.steps, a, b, c, d)
        if self.counterclockwise:
            self.drawingMethod(self.colorPalette, self.lengthMultiplier, -math.pi/2, self.steps, a, b, c, d)
        with bot.savedState():
            bot.stroke(0)
            bot.line(a, b)
            bot.line(c, d)
        dps(a, b, c, d)
        self.lastPoint = points[-1]

if __name__ == "__main__":

    from fontTools.pens.cocoaPen import CocoaPen
    def drawGlyph(glyph):
        if hasattr(glyph, "getRepresentation"):
            path = glyph.getRepresentation("defconAppKit.NSBezierPath")
        else:
            font = None
            if hasattr(glyph, "font"):
                font = glyph.font
            elif hasattr(glyph, "getParent"):
                font = glyph.getParent()
            pen = CocoaPen(font)
            glyph.draw(pen)
            path = pen.path
        bot.drawPath(path)

    from fontParts.world import OpenFont

    pen = CurvaturePen(lengthMultiplier=500, colorPalette=( (1,.8,0,.5), (1,.8,1,1)))
    cf = OpenFont("cubic.ufo")
    c_glyph = cf["A"]

    cf_alpha = OpenFont("cubic_a.ufo")
    c_glyph_alpha = cf_alpha["a"]

    qf = OpenFont("quad.ufo")
    q_glyph = qf["A"]

    qf_alpha = OpenFont("quad_a.ufo")
    q_glyph_alpha = qf_alpha["a"]

    bot.size(c_glyph.width,1000)
    bot.fill(None)
    bot.stroke(0,0,0,1)
    drawGlyph(c_glyph)
    bot.fill(0)
    bot.stroke(None)
    c_glyph.draw(pen)

    bot.newPage(c_glyph_alpha.width,1000)
    bot.fill(None)
    bot.stroke(0,0,0,1)
    drawGlyph(c_glyph_alpha)
    bot.fill(0)
    bot.stroke(None)
    c_glyph_alpha.draw(pen)

    bot.newPage(q_glyph.width,1000)
    bot.fill(None)
    bot.stroke(0,0,0,1)
    drawGlyph(q_glyph)
    bot.fill(0)
    bot.stroke(None)
    q_glyph.draw(pen)

    bot.newPage(q_glyph_alpha.width,1000)
    bot.fill(None)
    bot.stroke(0,0,0,1)
    drawGlyph(q_glyph_alpha)
    bot.fill(0)
    bot.stroke(None)
    q_glyph_alpha.draw(pen)

    bot.saveImage("test.pdf")