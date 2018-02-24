from kivy.properties import BooleanProperty, ObjectProperty
from kivy.logger import Logger
from kivy.resources import resource_add_path
import os
from functools import partial

from ELiDE.game import GameScreen, GameApp
from ELiDE.board import Pawn


resource_add_path(os.path.join(os.path.dirname(__file__), 'LPC_city_inside'))
resource_add_path(os.path.join(os.path.dirname(__file__), 'LPC_house_interior'))




class DunUniPlayView(GameScreen):
    player = ObjectProperty()
    character = ObjectProperty()
    class_time = BooleanProperty()
    sleepy = BooleanProperty()
    hungry = BooleanProperty()
    people_present = BooleanProperty()
    
    def go_to_class(self, *args):
        me = self.player.avatar['physical']
        if me.location.name == 'classroom':
            Logger.info("DunUniPlayView: already in classroom")
            return
        self.wait_travel('physical', me.name, 'classroom')

    def go_to_sleep(self, *args):
        myroom = self.player.stat['room']
        me = self.player.avatar['physical']
        if me.location != myroom:
            self.wait_travel_command(
                'physical', me.name, myroom.name, self.ensleep, 8, self.unsleep
            )
        else:
            self.wait_command(self.ensleep, 8, self.unsleep)

    def ensleep(self, *args):
        bed = self.player.stat['bed']
        self.player.avatar['physical'].location = bed
        self.character.stat['conscious'] = False

    def unsleep(self, *args):
        self.character.stat['conscious'] = True
        Logger.debug("DunUniPlayView: finished sleeping")

    def eat_food(self, *args):
        cafeteria = self.engine.character['physical'].place['cafeteria']
        me = self.player.avatar['physical']
        if me.location != cafeteria:
            self.wait_travel_command('physical', me.name, 'cafeteria', self.eneat, 1, self.uneat)
        else:
            self.wait_command(self.eneat, 1, self.uneat)

    def eneat(self, *args):
        self.character.stat['eating'] = True

    def uneat(self, *args):
        self.character.stat['eating'] = False
        Logger.debug("DunUniPlayView: finished eat_food")

    def socialize(self, *args):
        peeps = [
            thing for thing in self.player.avatar['physical'].location.contents()
            if thing.user and thing != self.player.avatar['physical']
        ]
        if not peeps:
            Logger.debug("DunUniPlayView: no one to socialize with")
            return
        peep = self.engine.choice(peeps)
        usr = peep.user
        Logger.debug("DunUniPlayView: going to talk to {} for a turn".format(usr.name))
        self.wait_command(partial(self.ensocialize, usr), 1, self.desocialize)

    def ensocialize(self, usr, *args):
        self.character.stat['talking_to'] = usr
        self.character.stat['talking_to'].stat['talking_to'] = self.character

    def desocialize(self, *args):
        del self.character.stat['talking_to'].stat['talking_to']
        del self.character.stat['talking_to']
        Logger.debug("DunUniPlayView: finished socialize")


class DunUniApp(GameApp):
    modules = ['util', 'emotion', 'world']
    inspector = True
    loglevel = 'debug'
    world_file = ':memory:'
