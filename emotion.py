# This file is part of Dungeon University:
# A school life simulator. In a dungeeon.
# Copyright (c) Zachary Spector, zacharyspector@gmail.com
"""Status effects to simulate cogent emotional states."""


def install(engine):
    @engine.action
    def rage_break_something(engine, character):
        me = character.avatar['physical']
        here = me.location
        stuff = [
            thing for thing in here.contents() if
            # things that are not avatars are inanimate
            not list(thing.users())
        ]
        breakthis = engine.choice(stuff)
        engine.function['deal_damage'](
            breakthis, character.stat['anger'], character.name
        )

    @engine.action
    def rage_hit_someone(engine, character):
        # TODO: account for stronger characters, weapons, etc
        me = character.avatar['physical']
        here = me.location
        peeps = [
            thing for thing in here.contents() if
            list(user for user in thing.users() if 'hp' in user)
        ]
        victim = next(
            user for user in engine.choice(peeps).users() if
            'hp' in user
        )
        # TODO: effects of being at low HP
        # The deal_damage function may delete the character
        # but not its avatar; that means it is no longer
        # anyone's body, just a corpse
        engine.function['deal_damage'](
            victim, character.stat['anger'], character.name
        )

    @engine.action
    def rage_damage_relationship(engine, character):
        # pick the nearest character I care about
        physical = engine.character['physical']
        social = engine.character['social']
        me_phys = character.avatar['physical']
        me_soc = character.avatar['social']
        closest = min(
            (me_phys.shortest_path_length(friend), friend)
            for friend in me_soc.successors()
