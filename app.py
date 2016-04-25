from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

import LiSE
import ELiDE


class DunUniApp(App):
    engine = ObjectProperty()
    board = ObjectProperty()
    screen = ObjectProperty()

    def build(self):
        self.procman = LiSE.proxy.EngineProcessManager(
            worlddb='DunUniWorld.db',
            codedb='DunUniCode.db'
        )
        self.engine = self.procman.start()
        self.screen = ScreenManager()
        self.board = 
