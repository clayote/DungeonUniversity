def install(engine):
    @engine.method
    def game_start(engine):
        player = engine.new_character('player')
        player.stat['wallpaper'] = 'uncle_mugen_tomb.jpg'
        phys = engine.new_character('physical')
        soc = engine.new_character('social')
