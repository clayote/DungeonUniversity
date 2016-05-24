def install(engine):
    @engine.method
    def game_start(engine):
        player = engine.new_character('player')
        phys = engine.new_character('physical')
        # I need distinct wallpaper for the map and the player's, um,
        # what exactly do I want the 'player' Character to show, again?
        phys.stat['wallpaper'] = player.stat['wallpaper'] = 'uncle_mugen_tomb.jpg'
        engine.add_character('social')
        # dorm 1
        rooms = [
            phys.new_place('room{}'.format(n), _x=0.1, _y=0.1+n/10)
            for n in range(1, 7)
        ]
        lounge = phys.new_place('lounge1', _x=0.2, _y=0.2)
        for room in rooms:
            lounge.two_way(room)
        for n, student in enumerate((
                'sam', 'kylie', 'jeff', 'catt', 'jim', 'meredith'
        )):
            engine.make_person(
                student, rooms[n], engine.character['social']  # everybody knows everyone
            )
