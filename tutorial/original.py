__author__ = 'guqiang'
# Game Flappy Bird

import simplegui
import random
import math


FPS = 60.0    # frame per sec
GROUND_SPEED = 190 / FPS  # px per frame
GROUND_HEIGHT = 0
GROUND_WIDTH = 384
GRAVITY = 35 / FPS  # px per frame
FLAP_SPEED = 510 / FPS  # px per frame
STAGE_WIDTH = 384
STAGE_HEIGHT = 448
BIRD_WIDTH = 43
BIRD_HEIGHT = 30
PIPE_WIDTH = 69
PIPE_GAP_X = 209
PIPE_GAP_Y = 128
FRAME_WIDTH = 384
FRAME_HEIGHT = GROUND_HEIGHT + STAGE_HEIGHT


class Stage:
    def __init__(self):
        self.width = STAGE_WIDTH
        self.height = STAGE_HEIGHT
        self.image = simplegui.load_image("https://github.com/ben7th/flappy-html5-bird/blob/gh-pages/ui/images/stage_sky.png?raw=true")

    def update(self):
        pass

    def draw(self, canvas):
        canvas.draw_image(self.image, [768/2, 896/2], [768, 896],
                          [self.width / 2, self.height / 2], [self.width, self.height])


class Score:
    def __init__(self):
        self.score = 0
        self.best_record = 0

    def start(self):
        self.score = 0

    def inc_score(self):
        self.score += 1

    def update_record(self):
        if self.score > self.best_record:
            self.best_record = self.score

    def draw_score(self, canvas):
        canvas.draw_text(str(self.score), [170, 50], 50, 'White', 'monospace')

    def draw_score_board(self, canvas):
        canvas.draw_text('GAME OVER', [80, 130], 40, 'White', 'monospace')
        canvas.draw_text('Current Score:' + str(self.score), [80, 160], 20, 'White', 'monospace')
        canvas.draw_text('Best Record:' + str(self.best_record), [80, 190], 20, 'White', 'monospace')


class Bird:
    def __init__(self):
        self.speed = 0
        self.gravity = 0
        self.is_dead = False
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.set_pos(99, 237)
        self.image = simplegui.load_image("https://github.com/ben7th/flappy-html5-bird/blob/gh-pages/ui/images/bird.png?raw=true")

    def start(self):
        self.speed = 0
        self.gravity = GRAVITY
        self.is_dead = False
        self.set_pos(99, 237)

    def draw(self, canvas):
        canvas.draw_image(self.image, [86/2, 60/2], [86, 60],
                          [self.center_x, self.center_y], [self.width, self.height])

    def update(self, stage):
        self.center_y -= self.speed
        if self.center_y > stage.height - self.height / 2.0:   # hit ground
            self.center_y = stage.height - self.height / 2.0
            self.speed = 0
            self.gravity = 0
        self.speed -= self.gravity

    def set_pos(self, x, y):
        self.center_x = x if x >= 0 else 0
        self.center_y = y if y >= 0 else 0

    def collide_detect(self, pipes, stage):
        if self.is_dead:
            pipes.is_stop = True
            return True
        # collide with ground
        if self.center_y >= stage.height - self.height / 2.0:
            self.is_dead = True
            pipes.is_stop = True
            return True
        # collide with pipe
        if len(pipes.pipes) > 0:
            p = pipes.pipes[0]
            if abs(p.center_x - self.center_x) < self.width / 2.0 + p.width / 2.0:
                if self.center_y < p.y_top + self.height / 2.0 or self.center_y > p.y_bottom - self.height / 2.0:
                    self.is_dead = True
                    pipes.is_stop = True
                    return True

    def flap(self):
        if self.is_dead:
            return
        self.gravity = GRAVITY
        self.speed = FLAP_SPEED


class Pipe:
    def __init__(self, pos):
        self.width = PIPE_WIDTH
        self.center_x = pos
        self.y_top = random.randrange(70, STAGE_HEIGHT - PIPE_GAP_Y - 70)
        self.y_bottom = self.y_top + PIPE_GAP_Y
        self.is_stop = True
        self.is_passed = False
        self.body_image = simplegui.load_image("https://raw.github.com/ben7th/flappy-html5-bird/gh-pages/ui/images/pipe_body.png")
        self.head1_image = simplegui.load_image("https://raw.github.com/ben7th/flappy-html5-bird/gh-pages/ui/images/pipe_head_1.png")
        self.head2_image = simplegui.load_image("https://raw.github.com/ben7th/flappy-html5-bird/gh-pages/ui/images/pipe_head_2.png")

    def update_pos(self):
        self.center_x -= GROUND_SPEED

    def set_pos(self):
        pass

    def draw(self, canvas):
        # head1
        canvas.draw_image(self.head1_image, [138/2, 64/2], [138, 64],
                          [self.center_x, self.y_top - 16], [69, 32])
        # body1
        canvas.draw_image(self.body_image, [127/2, 1/2], [127, 1],
                          [self.center_x, (self.y_top - 32)/2], [127/2, (self.y_top - 32)])
        # head2
        canvas.draw_image(self.head2_image, [138/2, 64/2], [138, 64],
                          [self.center_x, self.y_bottom + 16], [69, 32])
        # body2
        canvas.draw_image(self.body_image, [127/2, 1/2], [127, 1],
                          [self.center_x, (STAGE_HEIGHT/2 + self.y_bottom/2 + 16)],
                          [127/2, (STAGE_HEIGHT - self.y_bottom - 32)])


class Pipes:
    def __init__(self):
        self.gap_x = PIPE_GAP_X
        self.gap_y = PIPE_GAP_Y
        self.pipes = []     # a list of pipe

    def start(self):
        self.clear()

    def generate(self):
        if len(self.pipes) == 0:    # first pipe
            new_pipe_pos = STAGE_WIDTH * 2
        else:
            last_pipe = self.pipes[-1]
            new_pipe_pos = last_pipe.center_x + self.gap_x
        new_pipe = Pipe(new_pipe_pos)
        self.pipes.append(new_pipe)

    def update(self):
        #update pos of pipes
        for p in self.pipes:
            p.update_pos()
        # generate new pipe
        if len(self.pipes) < 3:
            self.generate()
        # remove old pipe
        pipe0 = self.pipes[0]
        if pipe0.center_x < - pipe0.width / 2.0:
            self.pipes.remove(pipe0)

    def draw(self, canvas):
        for p in self.pipes:
            p.draw(canvas)

    def clear(self):
        for p in self.pipes:
            self.pipes.remove(p)
        self.pipes = []

    def get_first_pipe_pos(self):
        for p in self.pipes:
            if not p.is_passed:
                return p.y_bottom


class Game:
    def __init__(self):
        self.stage = Stage()
        self.bird = Bird()
        self.score = Score()
        self.pipes = Pipes()
        self.frame = simplegui.create_frame("Flappy Bird", FRAME_WIDTH, FRAME_HEIGHT)
        self.game_is_over = False
        self.is_started = False
        self.is_robot_on = False
        self.register_handlers()

    def register_handlers(self):
        self.frame.set_draw_handler(draw_handler)
        self.frame.set_mouseclick_handler(click_handler)
        self.frame.set_keydown_handler(key_handler)
        self.frame.add_button('Start', start_button_handler)
        self.frame.add_button('Start with Robot', robot_button_handler)

    def start(self):
        self.bird.start()
        self.pipes.start()
        self.score.start()
        self.is_started = True
        self.game_is_over = False

    def ready(self):
        pass

    def over(self):
        pass

    def flap(self):
        if not self.game_is_over:
            self.bird.flap()

    def draw(self, canvas):
        self.stage.draw(canvas)
        self.pipes.draw(canvas)
        self.bird.draw(canvas)
        self.score.draw_score(canvas)
        if self.game_is_over:
            self.score.draw_score_board(canvas)

    def update(self):
        self.bird.update(self.stage)
        if self.is_robot_on:
            if self.bird.speed <= 0:
                if self.bird.center_y + self.bird.height / 2.0 - self.bird.speed > self.pipes.get_first_pipe_pos():
                    self.flap()
        if not self.game_is_over:
            self.pipes.update()
            self.score.update_record()
            self.update_score()
            self.stage.update()
            if self.bird.collide_detect(self.pipes, self.stage):
                self.game_is_over = True

    def update_score(self):
        if not self.game_is_over:
            pipe0 = self.pipes.pipes[0]
            if pipe0.center_x + pipe0.width / 2.0 < self.bird.center_x - self.bird.width / 2.0:
                if not pipe0.is_passed:
                    pipe0.is_passed = True
                    self.score.inc_score()


# global functions


def draw_handler(canvas):
    if game.is_started:
        game.update()
    game.draw(canvas)


def click_handler(pos):
    if 0 <= pos[0] <= FRAME_WIDTH and 0 <= pos[1] <= FRAME_HEIGHT:
        game.flap()


def key_handler(key):
    game.flap()
    pass


def start_button_handler():
    game.is_robot_on = False
    game.start()


def robot_button_handler():
    game.is_robot_on = True
    game.start()

game = Game()
game.frame.start()
