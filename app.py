from kivy.properties import BooleanProperty, ObjectProperty
from threading import Lock

from ELiDE.game import GameScreen, GameApp


class DunUniPlayView(GameScreen):
    player = ObjectProperty()
    character = ObjectProperty()
    class_time = BooleanProperty()
    sleepy = BooleanProperty()
    hungry = BooleanProperty()
    people_present = BooleanProperty()
    
    def __init__(self,  **kwargs):
        self._cmd_lock = Lock()
        super().__init__(**kwargs)

    def go_to_class(self, *args):
        self._cmd_lock.acquire()
        me = self.player.avatar['physical']
        classroom = self.engine.character['physical'].place['classroom']
        me.travel_to(classroom)
        while me.location != classroom:
            self.engine.next_tick('physical')
        self._cmd_lock.release()

    def go_to_sleep(self, *args):
        self._cmd_lock.acquire()
        myroom = self.player.stat['room']
        me = self.player.avatar['physical']
        if me.location != myroom:
            me.travel_to(myroom)
            while me.location != myroom:
                self.engine.next_tick()
        bed = self.player.stat['bed']
        me.location = bed
        self.character.stat['conscious'] = False
        for i in range(8):
            self.engine.next_tick()
        self.character.stat['conscious'] = True
        self._cmd_lock.release()

    def eat_food(self, *args):
        self._cmd_lock.acquire()
        cafeteria = self.engine.character['physical'].place['cafeteria']
        me = self.character.avatar['physical']
        if me.location != cafeteria:
            me.travel_to(cafeteria)
            while me.location != cafeteria:
                self.engine.next_tick()
        self.character.stat['eating'] = True
        self.engine.next_tick()
        self.character.stat['eating'] = False
        self._cmd_lock.release()

    def socialize(self, *args):
        self._cmd_lock.acquire()
        peeps = [thing for thing in self.character.avatar['physical'].contents() if thing.user]
        self.character.stat['talking_to'] = self.engine.choice(peeps).user
        self.character.stat['talking_to'].stat['talking_to'] = self.character
        self.engine.next_tick()
        self.character.stat['talking_to'].stat['talking_to'] = None
        self.character.stat['talking_to'] = None
        self._cmd_lock.release()


class DunUniApp(GameApp):
    modules = ['util', 'emotion', 'world']
    inspector = True
