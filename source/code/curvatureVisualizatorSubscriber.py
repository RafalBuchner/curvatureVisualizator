from curvatureGlyph_merz import CurvaturePen
import vanilla as vui
from AppKit import NSRoundRectBezelStyle
from fontTools.pens.transformPen import TransformPointPen, TransformPen
from fontTools.misc.transform import Transform
from displaySubscriber import DisplaySuscriber
from mojo import subscriber, events
from merz import MerzPen
from curvatureVisualizatorSettings import (
    internalGetDefault,
    internalSetDefault,
    extensionKeyStub,
    extensionID
)


# ====================================
# S U B S C R I B E R
# ====================================

class CurvatureVisualizatorSubscriber(DisplaySuscriber):
    debug = True

    title = "curvature visualizator"
    scale = None
    bgBaseLayer = None
    outlineType = None
    zoomVisualisation = None
    absoluteVisualisationSize = None
    visualisationSize = None
    showOptionsButtonInGlyphWindow = None
    clockwise, counterclockwise = None, None
    def build(self):
        self.loadDefaults()


        window = self.getGlyphEditor()
        self.backgroundContainer = window.extensionContainer(
            identifier=extensionKeyStub + "background",
            location="background",
            clear=True,
        )
        self.bgBaseLayer = self.backgroundContainer.appendBaseSublayer()

        # controls
        self.optionsGroup = vui.Group((0, -200, -0, -0))
        self.optionsGroup.button = vui.Button((-141-6, -35-8, 120, 22),
                                        "curvature options",
                                        callback=self.curvatureOptionsCallback)
        nsObj = self.optionsGroup.button.getNSButton()
        nsObj.setBezelStyle_( NSRoundRectBezelStyle )
        window.addGlyphEditorSubview(self.optionsGroup)
        self.showCurvatureOptions()
        events.addObserver(
            self, "extensionDefaultsChanged", extensionKeyStub + "defaultsChanged"
        )

    def loadDefaults(self):
        self.steps = internalGetDefault("divisionSteps_EditText_int")
        self.colorPalette = (internalGetDefault("fillColor_ColorWell"), internalGetDefault("strokeColor_ColorWell"))
        self.strokeWidth = internalGetDefault("strokeWidth_EditText_int")
        self.showOptionsButtonInGlyphWindow = internalGetDefault("showOptionsButtonInGlyphWindow_CheckBox")
        self.showMe = internalGetDefault("isVisible")
        self.zoomVisualisation = internalGetDefault("zoomVisualisation_CheckBox")
        self.absoluteVisualisationSize = internalGetDefault("visualisationSize_Slider_int")["value"]
        visualisationType = internalGetDefault("visualisationType_SegmentedButton_counterclockwise_clockwise_both")
#         print(
# f"""
# steps = {self.steps}
# colorPalette = {self.colorPalette}
# strokeWidth = {self.strokeWidth}
# showOptionsButtonInGlyphWindow = {self.showOptionsButtonInGlyphWindow}
# showMe = {self.showMe}
# zoomVisualisation = {self.zoomVisualisation}
# absoluteVisualisationSize = {self.absoluteVisualisationSize}
# visualisationType = {visualisationType}
# """
#         )
        if visualisationType == 2:
            self.clockwise, self.counterclockwise = True, True
        elif visualisationType == 1:
            self.clockwise, self.counterclockwise = True, False
        elif visualisationType == 0:
            self.clockwise, self.counterclockwise = False, True

    def destroy(self):
        self.backgroundContainer.clearSublayers()
        events.removeObserver(self, extensionKeyStub + "defaultsChanged")

    def toggleOn(self):
        if self.bgBaseLayer is None:
            return
        self.bgBaseLayer.setVisible(True)

    def toggleOff(self):
        if self.bgBaseLayer is None:
            return
        self.bgBaseLayer.setVisible(False)

    # # # # # # # # # # #
    # Option Button
    #
    @property
    def visualisationSize(self):
        value = self.absoluteVisualisationSize
        if self.zoomVisualisation:
            value *= 1/self.scale
        return value

    def glyphEditorDidScale(self, info):
        self.scale = info["scale"]
        if self.zoomVisualisation and self.pen is not None and self.showMe:
            self.pen.resetMerzPens()
            self.pen.setLengthMultiplier(self.visualisationSize) # faster than self.drawPath(info)
            self.drawPath(info)

    def curvatureOptionsCallback(self, sender):
        try:
            self.pop = vui.Popover((300, 170), preferredEdge='bottom', behavior='transient')

            y = 10
            self.pop.visualisationSizeText = vui.TextBox((10, y, -10, 20), 'visualisation size')

            y += 22+10
            sliderDefaults =internalGetDefault("visualisationSize_Slider_int")
            self.pop.visualisationSize_Slider_int = vui.Slider(
                (10, y, -10, 20),
                minValue=sliderDefaults.get("minValue"),
                maxValue=sliderDefaults.get("maxValue"),
                value=sliderDefaults.get("value"),
                callback=self.settingsCallback, continuous=True
            )

            y += 22+10
            self.pop.type = vui.TextBox((10, y, -10, 20), 'visualisation type')

            y += 22+10
            self.pop.visualisationType_SegmentedButton_counterclockwise_clockwise_both = vui.SegmentedButton((10, y, -10, 20),
                         [dict(title="counterclockwise"), dict(title="clockwise"), dict(title="both")],
                        callback=self.settingsCallback)
            self.pop.visualisationType_SegmentedButton_counterclockwise_clockwise_both.set(
                internalGetDefault("visualisationType_SegmentedButton_counterclockwise_clockwise_both")
            )

            y += 22+10
            self.pop.zoomVisualisation_CheckBox = vui.CheckBox((10, y, 240, 20),
                        "zoom visualisation",value=internalGetDefault("zoomVisualisation_CheckBox"),
                        callback=self.settingsCallback)

            self.pop.visualisationSize_Slider_int._id = "visualisationSize_Slider_int"
            self.pop.visualisationType_SegmentedButton_counterclockwise_clockwise_both._id = "visualisationType_SegmentedButton_counterclockwise_clockwise_both"
            self.pop.zoomVisualisation_CheckBox._id = "zoomVisualisation_CheckBox"
            self.pop.open(parentView=sender.getNSButton(), preferredEdge='top')
        except:
            import traceback
            print(traceback.format_exc())

    def settingsCallback(self, sender):
        if "_Slider" in sender._id:
            value = sender.get()
            if "_SliderInt" in sender._id:
                value = int(value)

            sliderDefaults =internalGetDefault("visualisationSize_Slider_int")
            value = dict(minValue=sliderDefaults.get("minValue"), maxValue=sliderDefaults.get("maxValue"), value=value)
            internalSetDefault(sender._id, value)

        elif "_CheckBox" in sender._id:
            internalSetDefault(sender._id, bool(sender.get()))

        else:
            internalSetDefault(sender._id, sender.get())

        events.postEvent(extensionID + ".defaultsChanged")

    def showCurvatureOptions(self):
        if self.showOptionsButtonInGlyphWindow:
            self.optionsGroup.show(self.showMe)
        else:
            self.optionsGroup.show(False)

    def extensionDefaultsChanged(self, event):
        self.loadDefaults()
        self.showCurvatureOptions()
        self.pen = CurvaturePen(steps=self.steps, lengthMultiplier=self.visualisationSize, clockwise=self.clockwise, counterclockwise=self.counterclockwise, colorPalette=self.colorPalette, strokeWidth=self.strokeWidth, parentLayer=self.bgBaseLayer)
        self.drawPath(dict(glyph=self.getGlyphEditor().getGlyph().asFontParts()))

    # def glyphEditorWantsContextualMenuItems(self, info):
    #     myMenuItems = [
    #         ("Curvature Type", self.contextualItemCallback)
    #     ]
    #     info["itemDescriptions"].extend(myMenuItems)

    # # # # # # # # # # #
    # Drawing
    #
    def setGlyph(self, info):
        self.scale = info["glyphEditor"].getGlyphViewScale()
        glyph = info["glyph"]
        self.pen = CurvaturePen(steps=self.steps, lengthMultiplier=self.visualisationSize, clockwise=self.clockwise, counterclockwise=self.counterclockwise, colorPalette=self.colorPalette, strokeWidth=self.strokeWidth, parentLayer=self.bgBaseLayer)

    def glyphEditorDidSetGlyph(self, info):
        self.setGlyph(info)
        self.drawPath(info)

    def glyphEditorDidKeyDown(self, info):
        try:
            self.pen.resetMerzPens()
            self.drawPath(info)
        except:
            import traceback
            print(traceback.format_exc())

    def glyphEditorDidUndo(self, info):
        try:
            self.pen.resetMerzPens()
            self.drawPath(info)
        except:
            import traceback
            print(traceback.format_exc())

    def glyphEditorDidMouseDrag(self, info):
        try:
            self.pen.resetMerzPens()
            self.drawPath(info)
        except:
            import traceback
            print(traceback.format_exc())

    def glyphEditorDidOpen(self, info):
        super().glyphEditorDidOpen(info)
        self.setGlyph(info)
        self.drawPath(info)
        self.showCurvatureOptions()

    pen = None
    def drawPath(self, info):
        if self.showMe:
            info["glyph"].draw(self.pen)
            self.pen.draw()

    def menuButtonWasPressed(self, nsMenuItem):
        if self.getButtonState():
            self.showMe = True
        else:
            self.showMe = False

        self.showCurvatureOptions()



subscriber.registerGlyphEditorSubscriber(CurvatureVisualizatorSubscriber)
