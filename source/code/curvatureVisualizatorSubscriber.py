from fontTools.pens.transformPen import TransformPointPen, TransformPen
from fontTools.misc.transform import Transform
from displaySubscriber import DisplaySuscriber
from mojo import subscriber
from merz import MerzPen
from settings import (
    internalGetDefault,
    internalSetDefault,
    extensionID,
    extensionKeyStub
)
from curvatureGlyph_merz import CurvaturePen


# ====================================
# S U B S C R I B E R
# ====================================

class CurvatureVisualizatorSubscriber(DisplaySuscriber):
    debug = True

    title = "curvature visualizator"
    bgBaseLayer = None

    def build(self):
        self.showMe = internalGetDefault("isVisible")
        window = self.getGlyphEditor()
        self.backgroundContainer = window.extensionContainer(
            identifier=extensionKeyStub + "background",
            location="background",
            clear=True,
        )
        self.bgBaseLayer = self.backgroundContainer.appendBaseSublayer()

    def toggleOn(self):
        if self.bgBaseLayer is None:
            return
        self.bgBaseLayer.setVisible(True)

    def toggleOff(self):
        if self.bgBaseLayer is None:
            return
        self.bgBaseLayer.setVisible(False)

    def glyphEditorDidKeyDown(self, info):
        self.drawPath(info)

    def glyphEditorDidUndo(self, info):
        self.drawPath(info)

    def glyphEditorDidMouseDrag(self, info):
        self.drawPath(info)

    def glyphEditorDidOpen(self, info):
        super().glyphEditorDidOpen(info)
        self.drawPath(info)

    def drawPath(self, info):
        glyph = info["glyph"]
        pen = CurvaturePen(steps=80, lengthMultiplier=2000, clockwise=True, counterclockwise=True, colorPalette=((1,.8,0,.5), (1,.8,0,.5)), strokeWidth=2, parentLayer=self.bgBaseLayer)
        glyph.draw(pen)
        pen.draw()


subscriber.registerGlyphEditorSubscriber(CurvatureVisualizatorSubscriber)
