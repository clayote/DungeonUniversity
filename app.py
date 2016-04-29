import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

import LiSE


class DunUniPlayView(BoxLayout):
    engine = ObjectProperty()
    character = ObjectProperty()
    class_time = BooleanProperty()
    sleepy = BooleanProperty()
    hungry = BooleanProperty()
    people_present = BooleanProperty()

    def go_to_class(self, *args):
        pass

    def go_to_sleep(self, *args):
        pass

    def eat_food(self, *args):
        pass

    def socialize(self, *args):
        pass


class DunUniApp(App):
    def build(self):
        # build the game if I haven't yet
        try:
            os.stat('DunUniWorld.db')
            os.stat('DunUniCode.db')
        except FileNotFoundError:
            try:
                os.remove('DunUniWorld.db')
            except FileNotFoundError:
                pass
            try:
                os.remove('DunUniCode.db')
            except FileNotFoundError:
                pass
            engine = LiSE.Engine('DunUniWorld.db', 'DunUniCode.db')
            import util
            import emotion
            for mod in (util, emotion):
                mod.install(engine)
            # this init function should probably be called
            # automagically by LiSE when it's launched in a
            # game-start-ish way
            engine.function['__init__'](engine)
            engine.close()
        self.procman = LiSE.proxy.EngineProcessManager(
            worlddb='DunUniWorld.db',
            codedb='DunUniCode.db'
        )
        self.engine = self.procman.start()
        self.screen = ScreenManager()
        self.playview = DunUniPlayView(
            engine=self.engine,
            character=self.engine.character['player']
        )
        self.screen.add_widget(self.playview)
        return self.screen


Builder.load_string("""
#: import Board ELiDE.board.Board
<DunUniPlayView>:
    BoxLayout:
        id: buttons
        orientation: 'vertical'
        size_hint_x: 0.3
        Button:
            id: go2class
            disabled: not root.class_time
            text: "Go to class"
            on_release: root.go_to_class()
        Button:
            id: sleep
            disabled: not root.sleepy
            text: "Sleep"
            on_release: root.go_to_sleep()
        Button:
            id: eat
            disabled: not root.hungry
            text: "Eat"
            on_release: root.eat_food()
        Button:
            id: soc
            disabled: not root.people_present
            text: "Socialize"
            on_release: root.socialize()
    Board:
        id: board
        engine: root.engine
        character: root.character
""")
