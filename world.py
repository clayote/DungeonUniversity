def install(engine):
    @engine.method
    def game_start(engine):
        phys = engine.new_character('physical')
        phys.stat['wallpaper'] = 'uncle_mugen_tomb.jpg'
        engine.add_character('social')
        # dorm 1
        rooms = [
            phys.new_place('room{}'.format(n), _x=0.1, _y=n/12, _image_paths=['atlas://city_inside/bed4'])
            for n in range(1, 8)
        ]
        lounge = phys.new_place('lounge1', _x=0.3, _y=0.3, _image_paths=['atlas://city_inside/small_carpet'])
        for room in rooms:
            lounge.two_way(room)
        for n, student in enumerate((
            'frances', 'josephine', 'sigmund', 'adolf', 'louise', 'edmund', 'boris'
        )):
            person = engine.make_person(
                student, rooms[n], icon='atlas://rltiles/dc-mon/' + student
            )
            person.stat['bed'] = rooms[n].new_thing('bed{}'.format(n))
        classroom = phys.new_place('classroom', _x=0.5, _y=0.5, _image_paths=['mpv-shot0002.png'])
        classroom.two_way(lounge)
        lounge.two_way(phys.new_place(
            'cafeteria', _x=0.5, _y=0.4,
            _image_paths=['atlas://interior/stovefront', 'atlas://interior/stovepot'],
            _offys=[0, 32]
        ))
