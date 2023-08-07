import drawBot as bot
from fontTools.pens.basePen import AbstractPen
from deriverateLib import interpolateTwoSetsOfValues, getCurvatureVisLineForT
import math, pprint



def dp(p, s=5):
    x, y = p
    r = s/2
    bot.oval(x-r,y-r,s,s)

def dps(*ps):
    for i,p in enumerate(ps):
        dp(p)
        a = (p[0]+7, p[1]-10)
        bot.text(f"{p}", a)

class CurvaturePen(AbstractPen):
    lastPoint = None
    def __init__(self):
        pass

    def moveTo(self, pt):
        self.lastPoint = pt
        dp(pt)

    def lineTo(self, pt):
        self.lastPoint = pt
        dp(pt)

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
            dps(*seg)

        self.lastPoint = points[-1]

    def curveTo(self, *points):
        self.lastPoint = points[-1]
        dps(*points)
        
        pass

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

    pen = CurvaturePen()
    cf = OpenFont("cubic.ufo")
    c_glyph = cf["A"]
    pen = CurvaturePen()
    qf = OpenFont("quad.ufo")
    q_glyph = qf["A"]

    bot.size(c_glyph.width,1000)
    bot.fill(None)
    bot.stroke(0,0,0,1)
    drawGlyph(c_glyph)
    bot.fill(0)
    bot.stroke(None)
    c_glyph.draw(pen)

    bot.newPage(q_glyph.width,1000)
    bot.fill(None)
    bot.stroke(0,0,0,1)
    drawGlyph(q_glyph)

    bot.fill(0)
    bot.stroke(None)
    q_glyph.draw(pen)

    bot.saveImage("test.pdf")