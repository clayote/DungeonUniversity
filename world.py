def install(engine):
    @engine.method
    def game_start(engine):
        phys = engine.new_character('physical')
        phys.stat['wallpaper'] = 'uncle_mugen_tomb.jpg'
        engine.add_character('social')
        # dorm 1
        rooms = [
            phys.new_place('room{}'.format(n), _x=0.1, _y=0.1+n/10)
            for n in range(1, 8)
        ]
        lounge = phys.new_place('lounge1', _x=0.2, _y=0.2)
        for room in rooms:
            lounge.two_way(room)
        for n, student in enumerate((
            'frances', 'josephine', 'sigmund', 'adolf', 'louise', 'edmund', 'boris'
        )):
            person = engine.make_person(
                student, rooms[n], icon='atlas://rltiles/dc-mon/' + student
            )
            person.stat['bed'] = rooms[n].new_thing('bed{}'.format(n))
        classroom = phys.new_place('classroom', _x=0.5, _y=0.5)
        classroom.two_way(lounge)
