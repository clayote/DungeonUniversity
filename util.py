# This file is part of Dungeon University:
# A school life simulator. In a dungeeon.
# Copyright (c) Zachary Spector, zacharyspector@gmail.com


def install(engine):
    @engine.function
    def damage_hp(what, amount, source='somewhere'):
        statmap = what.stat if hasattr(what, 'stat') else what
        if 'hp' not in statmap:
            what.engine.log("{} was destroyed by {}".format(
                what.name, source
            ))
            what.delete()
            return
        if isinstance(amount, str):
            amount = what.engine.dice(map(int, amount.split('d')))
        statmap['hp'] -= amount
        what.engine.log("{} took {} damage from {}".format(
            what.name, amount, source
        ))
        if statmap['hp'] <= what.engine.eternal.get('death_threshold', 0):
            what.engine.log("{} was destroyed by {}".format(
                what.name, source
            ))
            what.delete()

    @engine.function
    def damage_relationship(whom, whose, amount):
        pass
