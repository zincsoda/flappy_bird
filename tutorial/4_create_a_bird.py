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


BIRD_WIDTH = 43
BIRD_HEIGHT = 32
BIRD_IMAGE = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/bird.png"
class Bird:
    def __init__(self):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.center_x = 99
        self.center_y = 260
        self.image = simplegui.load_image(BIRD_IMAGE)

    def draw(self, canvas):
        canvas.draw_image(self.image,
                          [BIRD_WIDTH / 2, BIRD_HEIGHT / 2],
                          [BIRD_WIDTH, BIRD_HEIGHT],
                          [self.center_x, self.center_y],
                          [BIRD_WIDTH, BIRD_HEIGHT])

GAME_WIDTH = 384
GAME_HEIGHT = 448
class Game:
    def __init__(self):
        self.frame = simplegui.create_frame("Flappy Bird", GAME_WIDTH, GAME_HEIGHT)
        self.frame.start()
        self.background = Background()
        self.bird = Bird()
        self.register_handlers()


    def draw(self, canvas):
        self.background.draw(canvas)
        self.bird.draw(canvas)

    def register_handlers(self):
        self.frame.set_draw_handler(self.draw)


game = Game()
