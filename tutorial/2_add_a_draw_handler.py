import simplegui
import time

GAME_WIDTH = 384
GAME_HEIGHT = 448
class Game:
    def __init__(self):
        self.frame = simplegui.create_frame("Flappy Bird", GAME_WIDTH, GAME_HEIGHT)
        self.frame.start()
        self.register_handlers()

    def draw(self, canvas):
        print time.time()

    def register_handlers(self):
        self.frame.set_draw_handler(self.draw)


game = Game()
