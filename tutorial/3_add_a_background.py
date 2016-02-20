import simplegui

GAME_WIDTH = 384
GAME_HEIGHT = 448

BACKGROUND_SKY = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/stage_sky.png"


class Background:
    def __init__(self):
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.background = simplegui.load_image(BACKGROUND_SKY)

    def draw(self, canvas):
        canvas.draw_image(self.background, [768/2, 896/2],
                          [768, 896], [self.width / 2, self.height / 2],
                          [self.width, self.height])

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
