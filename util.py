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

    @engine.method
    def make_person(engine, who, where, who_knows=[], icon=None):
        me = engine.new_character(who)
        phys = engine.character['physical']
        my_body = phys.new_thing(who, where)
        if icon:
            my_body['_image_paths'] = [icon]
        me.add_avatar(my_body)
        assert 'physical' in me.avatar and my_body.name in me.avatar['physical'], "Failed adding physical avatar"
        me.stat['room'] = where
        soc = engine.character['social']
        my_brand = soc.new_place(who)
        me.add_avatar(my_brand)
        assert 'social' in me.avatar and my_brand.name in me.avatar['social'], "Failed adding social avatar"
        assert 'physical' in me.avatar and my_body.name in me.avatar['physical'], "Forgot physical avatar"
        for pal in who_knows:
            pally = soc.place[pal]
            pally.two_way(my_brand)
        return me
