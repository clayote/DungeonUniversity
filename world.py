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
        lounge = phys.new_place('lounge1', _x=0.3, _y=0.3, _image_paths=['atlas://city_inside/small_carpet'])
        student_body = engine.new_character('student_body')
        schools = ('life', 'death', 'sense', 'mind')
        for n, school in enumerate(schools, start=1):
            classroom = phys.new_place(school + '_classroom', _x=0.5, _y=n*0.1, _image_paths=['mpv-shot0002.png'])
            classroom.two_way(lounge)
        for n, student in enumerate((
            'frances', 'josephine', 'sigmund', 'louise', 'edmund', 'boris', 'erica'
        )):
            room = phys.new_place('room{}'.format(n), _x=0.1, _y=n / 12)
            lounge.two_way(room)
            person = engine.make_person(
                student, room, icon='atlas://rltiles/dc-mon/' + student
            )
            person.stat['conscious'] = True
            person.stat['bed'] = room.new_thing('bed{}'.format(n), _image_paths=['atlas://city_inside/bed4'])
            person.stat['classroom'] = phys.node[schools[n%4] + '_classroom']
            body = person.avatar['physical'].only
            student_body.add_avatar(body)
        lounge.two_way(phys.new_place(
            'cafeteria', _x=0.4, _y=0.4,
            _image_paths=['atlas://interior/stovefront', 'atlas://interior/stovepot'],
            _offys=[0, 32]
        ))
        # Make the player character 'truant' so that they don't automatically go to class.
        # Eventually they'll have the option to automate this but likely via some other
        # mechanism than the go_to_class rule -- maybe a player-generated rule.
        engine.character['josephine'].stat['truant'] = True

        @student_body.avatar.rule
        def go_to_class(node):
            # There's just one really long class every day.
            node['arrive_at_class'] = node.travel_to(node.user.stat['classroom'])

        @go_to_class.trigger
        def absent(node):
            return node.location != node.user.stat['classroom']

        @go_to_class.prereq
        def conscious(node):
            return node.user.stat['conscious']

        @go_to_class.prereq
        def class_in_session(node):
            return 8 <= node.engine.character['physical'].stat['hour'] < 15

        @go_to_class.prereq
        def not_going_to_class(node):
            return 'arrive_at_class' not in node or node['arrive_at_class'] > node.engine.turn

        @go_to_class.prereq
        def not_truant(node):
            return not node.user.stat.get('truant', False)

        @student_body.avatar.rule
        def leave_class(node):
            # TODO more interesting selection of after-class activities
            node.travel_to(node.user.stat['room'])

        @leave_class.trigger
        def in_classroom_after_class(node):
            phys = node.character
            return node.location.name.endswith('classroom') \
                   and phys.stat['hour'] >= 15

        leave_class.prereq('not_truant')