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

# ====================================
# S U B S C R I B E R
# ====================================       

class CurvatureVisualizatorSubscriber(DisplaySuscriber):
    debug = True

    title = "curvature visualizator" 
    curvaturePath = None
    
    def build(self):
        self.showMe = internalGetDefault("isVisible")
        window = self.getGlyphEditor()
        self.backgroundContainer = window.extensionContainer(
            identifier=extensionKeyStub + "background",
            location="background",
            clear=True,
        )
        self.bgBaseLayer = self.backgroundContainer.appendBaseSublayer()
        self.curvaturePath = self.bgBaseLayer.appendPathSublayer(
            fillColor=(1, 0, 0, 0.5), visible=False
        )

    def toggleOn(self):
        if self.curvaturePath is None:
            return
        self.curvaturePath.setVisible(True)

    def toggleOff(self):
        if self.curvaturePath is None:
            return
        self.curvaturePath.setVisible(False)

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
        merzPen = MerzPen()
        n_glyph = RGlyph()
        n_glyphPen = n_glyph.getPen()
        glyph.draw(n_glyphPen)
        n_glyph.moveBy((100,100))
        n_glyph.draw(merzPen)

        self.curvaturePath.setPath( merzPen.path )
        

subscriber.registerGlyphEditorSubscriber(CurvatureVisualizatorSubscriber)