from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty

from ELiDE.game import GameScreen, GameApp


class DunUniPlayView(GameScreen):
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


class DunUniApp(GameApp):
    modules = ['util', 'emotion', 'world']
    name = 'DunUni'


Builder.load_string("""
#: import Board ELiDE.board.Board
<DunUniPlayView>:
    BoxLayout:
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
            size_hint_x: 0.6
            engine: root.engine
            character: root.character
<Screens>:
    DunUniPlayView:
        name: 'play'
        character: self.engine.character['player']
""")
