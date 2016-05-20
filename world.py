def install(engine):
    @engine.method
    def game_start(engine):
        player = engine.new_character('player')
        player.stat['wallpaper'] = 'uncle_mugen_tomb.jpg'
        phys = engine.new_character('physical')
        engine.add_character('social')
        # dorm 1
        rooms = [
            phys.new_place('room{}'.format(n), _x=0.1, _y=0.1+n/10)
            for n in range(1, 7)
        ]
        lounge = phys.new_place('lounge1', _x=0.2, _y=0.2)
        for room in rooms:
            lounge.two_way(room)
        for n, student in enumerate(
                'sam', 'kylie', 'jeff', 'catt', 'jim', 'meredith'
        ):
            engine.function['make_person'](
                engine, student, rooms[n],
                engine.character['social']  # everybody knows everyone
            )
