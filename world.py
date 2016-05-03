def install(engine):
    @engine.function
    def __init__(engine):
        player = engine.new_character('player')
        phys = engine.new_character('physical')
        soc = engine.new_character('social')
