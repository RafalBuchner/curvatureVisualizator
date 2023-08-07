import ezui



class DemoController(ezui.WindowController):

    def build(self):
        content = """
        = ScrollingVerticalStack
        [_ ?]

        * Box
        > * Accordion: Stem Plow @accordion1
        > > ----------
        > > !- This is caption text.
        > > (Button 1)              @button1
        # > > !* This is caption text.
        > > (Button 2)              @button2
        > > !* This is footnote text.

        * Box
        > * Accordion: Accordion 1 @accordion1
        > > ----------
        > > (Button 1)              @button1
        > > !- This is caption text.
        > > (Button 2)              @button2
        > > !* This is footnote text.

        * Box
        > * Accordion: Accordion 1 @accordion1
        > > ----------
        > > (Button 1)              @button1
        > > !- This is caption text.
        > > (Button 2)              @button2
        > > !* This is footnote text.


        """
        descriptionData = dict(
        )
        self.w = ezui.EZWindow(
            title="Demo",
            size=(200, 200),
            minSize=(200,200),
            content=content,
            descriptionData=descriptionData,
            controller=self
        )

    def started(self):
        self.w.open()

DemoController()
