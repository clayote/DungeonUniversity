from kivy.properties import BooleanProperty, ObjectProperty
from kivy.logger import Logger

from ELiDE.game import GameScreen, GameApp


class DunUniPlayView(GameScreen):
    player = ObjectProperty()
    character = ObjectProperty()
    class_time = BooleanProperty()
    sleepy = BooleanProperty()
    hungry = BooleanProperty()
    people_present = BooleanProperty()
    
    def go_to_class(self, *args):
        me = self.player.avatar['physical']
        classroom = self.engine.character['physical'].place['classroom']
        me.travel_to(classroom)
        n = 0
        while me.location != classroom:
            Logger.debug("DunUniPlayView: {}th tick travelling to classroom".format(n))
            self.engine.next_tick(chars=['physical'])
            n += 1
        Logger.debug("DunUniPlayView: finished go_to_class")

    def go_to_sleep(self, *args):
        myroom = self.player.stat['room']
        me = self.player.avatar['physical']
        if me.location != myroom:
            me.travel_to(myroom)
            n = 0
            while me.location != myroom:
                Logger.debug("DunUniPlayView: {}th tick travelling to my room".format(n))
                n += 1
                self.engine.next_tick(chars=['physical'])
            Logger.debug("DunUniPlayView: moved {} to {}".format(me,  myroom))
        bed = self.player.stat['bed']
        me.location = bed
        self.character.stat['conscious'] = False
        n = 0
        for i in range(8):
            Logger.debug("DunUniPlayView: {}th tick unconscious".format(n))
            self.engine.next_tick(chars=['physical'])
        self.character.stat['conscious'] = True
        Logger.debug("DunUniPlayView: finished go_to_sleep")

    def eat_food(self, *args):
        cafeteria = self.engine.character['physical'].place['cafeteria']
        me = self.player.avatar['physical']
        if me.location != cafeteria:
            me.travel_to(cafeteria)
            while me.location != cafeteria:
                self.engine.next_tick(chars=['physical'])
        self.character.stat['eating'] = True
        self.engine.next_tick(chars=['physical'])
        self.character.stat['eating'] = False
        Logger.debug("DunUniPlayView: finished eat_food")

    def socialize(self, *args):
        peeps = [thing for thing in self.player.avatar['physical'].contents() if thing.user]
        if not peeps:
            self._cmd_lock_release()
            Logger.debug("DunUniPlayView: no one to socialize with")
            return
        self.character.stat['talking_to'] = self.engine.choice(peeps).user
        self.character.stat['talking_to'].stat['talking_to'] = self.character
        self.engine.next_tick(chars=['physical'])
        self.character.stat['talking_to'].stat['talking_to'] = None
        self.character.stat['talking_to'] = None
        Logger.debug("DunUniPlayView: finished socialize")


class DunUniApp(GameApp):
    modules = ['util', 'emotion', 'world']
    inspector = True
    world_file = code_file = ':memory:'
