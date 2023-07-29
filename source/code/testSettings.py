
import vanilla as vui
import AppKit, pprint
import sys

extensionID = "com.rafalbuchner.CurveVisualizator"
extensionKeyStub = extensionID + "."

__defaults__ = {
    extensionKeyStub + "isVisible": False,
    extensionKeyStub + "visualisationType_SegmentedButton_counterclockwise_clockwise_both": 0,
    extensionKeyStub + "divisionSteps_EditText_int": 77,
    extensionKeyStub + "strokeWidth_EditText_int": 2,
    extensionKeyStub + "showOptionsButtonInGlyphWindow_CheckBox": True,
    extensionKeyStub + "zoomVisualisation_CheckBox": False,
    extensionKeyStub + "visualisationSize_Slider_int": dict(minValue=0,maxValue=8000,value=1600),
    # extensionKeyStub + "fillColor_ColorWell": (1,.8,0,.5),
    # extensionKeyStub + "strokeColor_ColorWell": (1,.8,0,.1),
}


if "RoboFont" in sys.executable:
    from mojo.extensions import (
        registerExtensionDefaults,
        getExtensionDefault,
        setExtensionDefault
    )
    def internalRegisterDefaults():
        registerExtensionDefaults(__defaults__)

    def internalGetDefault(key):
        key = extensionKeyStub + key
        return getExtensionDefault(key)

    def internalSetDefault(key, value):
        pass
        key = extensionKeyStub + key
        setExtensionDefault(key, value)

    internalRegisterDefaults()
else:
    def internalGetDefault(key):
        key = extensionKeyStub + key
        return __defaults__.get(key)

def camelCaseToSpaced(txt):
    return ''.join(map(lambda x: x if x.islower() else " "+x, txt))

def convertRGBA_to_NSColor(color):
    if isinstance(color, AppKit.NSColor):
        return color
    return AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(*color)

def convertNSColor_to_RGBA(color):
    color = color.colorUsingColorSpace_(AppKit.NSColorSpace.genericRGBColorSpace())
    r = color.redComponent()
    g = color.greenComponent()
    b = color.blueComponent()
    a = color.alphaComponent()
    return (r, g, b, a)

class GridViewExample:
    def __init__(self):
        items = []
        for keyEntry in __defaults__:
            key = keyEntry.split(".")[-1]
            if "_" not in keyEntry:
                continue

            title = camelCaseToSpaced(key.split("_")[0]).lower()
            className = key.split("_")[1]
            ClassType = vui.__dict__[className]
            args = ("auto",)
            kwargs = dict(callback=self.objCallback)
            if key.count("_") > 2:
                classArgs = key.split("_")[2:]

            if className == "SegmentedButton":
                args = ("auto", [dict(title=n) for n in classArgs])
                value = internalGetDefault(key)

            elif className == "Slider":
                sliderData = internalGetDefault(key)
                print(sliderData)
                kwargs = dict(maxValue=sliderData.get("maxValue",100),minValue=sliderData.get("minValue",0))
                print(kwargs)
                kwargs["callback"] = self.objCallback
                value = internalGetDefault(key).get("value")

            elif className == "CheckBox":
                value = internalGetDefault(key)
                args  = ("auto", title)
                title = " "
            elif className == "Color":
                color = internalGetDefault(key)
                value = convertRGBA_to_NSColor(color)
            else:
                value = internalGetDefault(key)


            obj = ClassType(*args,**kwargs)
            obj._id = key
            obj.set(value)
            setattr(self, key, obj)
            i = dict(
                title=title,
                obj=obj
            )
            items.append(i)

        rows = []
        for item in items:
            title, obj = item["title"], item["obj"]
            titleObj = vui.TextBox("auto", title)
            setattr(self, title.replace(" ","_")+"_TextBox", obj)
            rows.append(dict(cells=[dict(view=titleObj), dict(view=obj)]))

        contents = rows




        self.w = vui.Window((500, 200), minSize=(500,200))
        self.w.box = vui.Box((10,10,-10,-10))
        self.w.box.gridView = vui.GridView(
            (10, 10, -10, -10),
            contents=contents,
            rowSpacing=10,
            rowPadding=(0, 0),
            rowPlacement="top",
            rowAlignment="firstBaseline",
            columnDescriptions=[
                dict(
                    columnPlacement="trailing",
                    width=200
                ),
                dict(
                    columnPlacement="leading",
                    width=300
                )
            ],
            columnSpacing=10,
            columnPadding=(0, 0),
            columnPlacement="leading",

        )

        self.w.open()

    def objCallback(self, sender):
        print(sender, sender.get())


#GridViewExample()

if __name__ == "__main__" and "RoboFont" not in sys.executable:
    from vanilla.test.testTools import executeVanillaTest
    executeVanillaTest(GridViewExample)
