import simplegui

GAME_WIDTH = 384
GAME_HEIGHT = 448
BIRD_WIDTH = 43
BIRD_HEIGHT = 30
BACKGROUND_SKY = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/stage_sky.png"
BIRD = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/bird.png"

class Background:
    def __init__(self):
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.background = simplegui.load_image(BACKGROUND_SKY)

    def draw(self, canvas):
        canvas.draw_image(self.background, [768/2, 896/2],
                          [768, 896], [self.width / 2, self.height / 2],
                          [self.width, self.height])

class Bird:
    def __init__(self):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.set_pos(99, 237)
        self.image = simplegui.load_image(BIRD)

    def draw(self, canvas):
        canvas.draw_image(self.image, [86/2, 60/2], [86, 60],
                          [self.center_x, self.center_y], [self.width, self.height])
    def set_pos(self, x, y):
        self.center_x = x if x >= 0 else 0
        self.center_y = y if y >= 0 else 0

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
