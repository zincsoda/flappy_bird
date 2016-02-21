import simplegui

GAME_WIDTH = 384
GAME_HEIGHT = 448
BACKGROUND_WIDTH = 768
BACKGROUND_HEIGHT = 896
BIRD_WIDTH = 43
BIRD_HEIGHT = 30
BACKGROUND_SKY = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/stage_sky.png"
BIRD = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/bird.png"
SPLASH_IMAGE = "https://raw.githubusercontent.com/sourabhv/FlapPyBird/master/assets/sprites/message.png"

class Background:
    def __init__(self):
        self.image_width = BACKGROUND_WIDTH
        self.image_height = BACKGROUND_HEIGHT
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.background = simplegui.load_image(BACKGROUND_SKY)

    def draw(self, canvas):
        canvas.draw_image(self.background,
                          [self.image_width / 2, self.image_height / 2],
                          [self.image_width, self.image_height],
                          [self.width / 2, self.height / 2],
                          [self.width, self.height])

class Splash:
    def __init__(self):
        self.image_width = 184
        self.image_height = 267
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.splash = simplegui.load_image(SPLASH_IMAGE)

    def draw(self, canvas):
        canvas.draw_image(self.splash,
                          [self.image_width / 2, self.image_height / 2],
                          [self.image_width, self.image_height],
                          [GAME_WIDTH / 2, GAME_HEIGHT / 2],
                          [self.image_width, self.image_height])
    def hide(self):
        self.splash = None

class Bird:
    def __init__(self):
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.set_pos(99, 260)
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
        self.register_handlers()
        self.game_is_started = False
        self.background = Background()
        self.bird = Bird()
        self.splash = Splash()

    def draw(self, canvas):
        self.background.draw(canvas)
        self.bird.draw(canvas)
        if not self.game_is_started:
            self.splash.draw(canvas)

    def key_pressed(self, key):
        if not self.game_is_started:
            self.splash.hide()
            self.game_is_started = True

    def register_handlers(self):
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.key_pressed)


game = Game()
