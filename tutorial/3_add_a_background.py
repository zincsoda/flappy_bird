import simplegui


BACKGROUND_WIDTH = 768
BACKGROUND_HEIGHT = 896
BACKGROUND_IMAGE = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/stage_sky.png"
class Background:
    def __init__(self):
        self.background_image = simplegui.load_image(BACKGROUND_IMAGE)

    def draw(self, canvas):
        canvas.draw_image(self.background_image,
                          [BACKGROUND_WIDTH / 2, BACKGROUND_HEIGHT / 2],
                          [BACKGROUND_WIDTH, BACKGROUND_HEIGHT],
                          [GAME_WIDTH / 2, GAME_HEIGHT / 2],
                          [GAME_WIDTH, GAME_HEIGHT])


GAME_WIDTH = 384
GAME_HEIGHT = 448
class Game:
    def __init__(self):
        self.frame = simplegui.create_frame("Flappy Bird", GAME_WIDTH, GAME_HEIGHT)
        self.frame.start()
        self.background = Background()
        self.register_handlers()


    def draw(self, canvas):
        self.background.draw(canvas)

    def register_handlers(self):
        self.frame.set_draw_handler(self.draw)


game = Game()
