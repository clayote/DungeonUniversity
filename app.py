from kivy.properties import BooleanProperty, ObjectProperty

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
        while me.location != classroom:
            self.engine.next_tick('physical')

    def go_to_sleep(self, *args):
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

    def eat_food(self, *args):
        cafeteria = self.engine.character['physical'].place['cafeteria']
        me = self.character.avatar['physical']
        if me.location != cafeteria:
            me.travel_to(cafeteria)
            while me.location != cafeteria:
                self.engine.next_tick()
        self.character.stat['eating'] = True
        self.engine.next_tick()
        self.character.stat['eating'] = False

    def socialize(self, *args):
        peeps = [thing for thing in self.character.avatar['physical'].contents() if thing.user]
        self.character.stat['talking_to'] = self.engine.choice(peeps).user
        self.character.stat['talking_to'].stat['talking_to'] = self.character
        self.engine.next_tick()
        self.character.stat['talking_to'].stat['talking_to'] = None
        self.character.stat['talking_to'] = None


class DunUniApp(GameApp):
    modules = ['util', 'emotion', 'world']
    inspector = True
