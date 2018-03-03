def install(engine):
    @engine.method
    def game_start(engine):
        phys = engine.new_character('physical')
        phys.stat['wallpaper'] = 'uncle_mugen_tomb.jpg'
        phys.stat['hour'] = 0

        @phys.rule(always=True)  # runs every turn regardless of the situation
        def time_passes(character):
            character.stat['hour'] = (character.stat['hour'] + 1) % 24


        engine.add_character('social')
        # dorm 1
        rooms = [
            phys.new_place('room{}'.format(n), _x=0.1, _y=n/12)
            for n in range(1, 8)
        ]
        lounge = phys.new_place('lounge1', _x=0.3, _y=0.3, _image_paths=['atlas://city_inside/small_carpet'])
        for room in rooms:
            lounge.two_way(room)
        student_body = engine.new_character('student_body')
        for n, student in enumerate((
            'frances', 'josephine', 'sigmund', 'louise', 'edmund', 'boris', 'erica'
        )):
            person = engine.make_person(
                student, rooms[n], icon='atlas://rltiles/dc-mon/' + student
            )
            person.stat['bed'] = rooms[n].new_thing('bed{}'.format(n), _image_paths=['atlas://city_inside/bed4'])
            body = person.avatar['physical'].only
            student_body.add_avatar(body)
        classroom = phys.new_place('classroom', _x=0.5, _y=0.5, _image_paths=['mpv-shot0002.png'])
        classroom.two_way(lounge)
        lounge.two_way(phys.new_place(
            'cafeteria', _x=0.5, _y=0.4,
            _image_paths=['atlas://interior/stovefront', 'atlas://interior/stovepot'],
            _offys=[0, 32]
        ))

        @student_body.avatar.rule
        def go_to_class(node):
            # There's just one really long class every day.
            node['arrive_at_class'] = node.travel_to(node.character.place['classroom'])

        @go_to_class.trigger
        def absent(node):
            return node.location != node.character.place['classroom']

        @go_to_class.prereq
        def class_in_session(node):
            return 8 <= node.engine.character['physical'].stat['hour'] < 15

        @go_to_class.prereq
        def not_going_to_class(node):
            return 'arrive_at_class' not in node or node['arrive_at_class'] > node.engine.turn

        @student_body.avatar.rule
        def leave_class(node):
            for user in node.users.values():
                if user.name != 'student_body':
                    node.travel_to(user.stat['room'])
                    return

        @leave_class.trigger
        def in_classroom_after_class(node):
            phys = node.character
            return node.location == phys.place['classroom'] \
                   and phys.stat['hour'] >= 15