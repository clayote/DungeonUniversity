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
