import simplegui
import random

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

SCORE_SOUND = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/score.wav"
class Score:
    def __init__(self):
        self.score = 0
        self.score_sound = simplegui.load_sound(SCORE_SOUND)

    def score_a_point(self):
        self.score_sound.rewind()
        self.score_sound.play()
        print "Score!"
        self.score += 1

    def draw_score(self, canvas):
        canvas.draw_text(str(self.score), [170, 50], 50, 'White', 'monospace')

    def draw_score_board(self, canvas):
        canvas.draw_text('GAME OVER', [80, 130], 40, 'White', 'monospace')
        canvas.draw_text('Current Score:' + str(self.score), [80, 160], 20, 'White', 'monospace')

BIRD_WIDTH = 43
BIRD_HEIGHT = 32
BIRD_IMAGE = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/bird.png"
GRAVITY = 0.6
FLAP_SPEED = 8.5
FLAP_SOUND = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/flap.wav"
class Bird:
    def __init__(self):
        self.center_x = 99
        self.center_y = 260
        self.speed = 0
        self.gravity = 0
        self.image = simplegui.load_image(BIRD_IMAGE)
        self.flap_sound = simplegui.load_sound(FLAP_SOUND)
        self.is_dead = False

    def draw(self, canvas):
        self.update_position()
        canvas.draw_image(self.image,
                          [BIRD_WIDTH / 2, BIRD_HEIGHT / 2],
                          [BIRD_WIDTH, BIRD_HEIGHT],
                          [self.center_x, self.center_y],
                          [BIRD_WIDTH, BIRD_HEIGHT])

    def update_position(self):
        self.center_y -= self.speed
        if self.center_y > GAME_HEIGHT - BIRD_HEIGHT / 2.0:   # hit ground
            self.center_y = GAME_HEIGHT - BIRD_HEIGHT / 2.0
            self.speed = 0
            self.gravity = 0
        self.speed -= self.gravity


    def flap(self):
        if self.is_dead:
            return
        self.gravity = GRAVITY
        self.speed = FLAP_SPEED
        self.flap_sound.rewind()
        self.flap_sound.play()

    def crash(self, nearest_pipe):
        if self.is_dead:
            return

        if self.center_y >= GAME_HEIGHT - BIRD_HEIGHT / 2.0:
            return True

        if (abs(nearest_pipe.center_x - self.center_x) < BIRD_WIDTH / 2.0 + PIPE_HEAD_WIDTH / 2.0) and \
           ((self.center_y - (BIRD_HEIGHT / 2) + 1 < nearest_pipe.y_top) or \
           (self.center_y + (BIRD_HEIGHT / 2) - 1 > nearest_pipe.y_bottom)):
            print "nearest_pipe.center_x:", nearest_pipe.center_x
            print "PIPE_HEAD_WIDTH / 2:", PIPE_HEAD_WIDTH / 2
            print "self.center_x:", self.center_x
            print "BIRD_WIDTH / 2:", BIRD_WIDTH / 2
            return True

    def kill(self):
        self.gravity = 0
        self.speed = 0
        self.is_dead = True

PIPE_BODY_WIDTH = 64
PIPE_HEAD_WIDTH = 69
PIPE_HEAD_HEIGHT = 32
PIPE_OPENING_HEIGHT = 128
PIPE_HEAD_HEIGHT = 32
PIPE_BODY_IMAGE = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/pipe_body.png"
PIPE_HEAD_DOWN_IMAGE = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/pipe_down_head.png"
PIPE_HEAD_UP_IMAGE = "https://raw.githubusercontent.com/zincsoda/flappy_bird/master/pipe_up_head.png"
GROUND_SPEED = 3
class Pipe:
    def __init__(self, pos):
        self.center_x = pos
        self.y_top = random.randrange(PIPE_HEAD_HEIGHT * 2, GAME_HEIGHT - PIPE_OPENING_HEIGHT - (PIPE_HEAD_HEIGHT * 2))
        self.y_bottom = self.y_top + PIPE_OPENING_HEIGHT
        self.is_stop = True
        self.is_passed = False
        self.pipe_body_image = simplegui.load_image(PIPE_BODY_IMAGE)
        self.pipe_head_down_image = simplegui.load_image(PIPE_HEAD_DOWN_IMAGE)
        self.pipe_head_up_image = simplegui.load_image(PIPE_HEAD_UP_IMAGE)
        self.speed = GROUND_SPEED
        self.is_passed = False

    def draw(self, canvas):
        self.update_position()
        # Top Pipe Body
        canvas.draw_image(self.pipe_body_image,
                          [PIPE_BODY_WIDTH / 2, 1 / 2],
                          [PIPE_BODY_WIDTH, 1],
                          [self.center_x, (self.y_top - PIPE_HEAD_HEIGHT) / 2],
                          [PIPE_BODY_WIDTH, (self.y_top - PIPE_HEAD_HEIGHT)])

        # Top Pipe Head
        canvas.draw_image(self.pipe_head_down_image,
                          [PIPE_HEAD_WIDTH/2, PIPE_HEAD_HEIGHT/2],
                          [PIPE_HEAD_WIDTH, PIPE_HEAD_HEIGHT],
                          [self.center_x, self.y_top - (PIPE_HEAD_HEIGHT / 2)],
                          [PIPE_HEAD_WIDTH, PIPE_HEAD_HEIGHT])
        # Bottom Pipe Head
        canvas.draw_image(self.pipe_head_up_image,
                          [PIPE_HEAD_WIDTH/2, PIPE_HEAD_HEIGHT/2],
                          [PIPE_HEAD_WIDTH, PIPE_HEAD_HEIGHT],
                          [self.center_x, self.y_bottom + (PIPE_HEAD_HEIGHT / 2)],
                          [PIPE_HEAD_WIDTH, PIPE_HEAD_HEIGHT])
        # Bottom Pipe Body
        canvas.draw_image(self.pipe_body_image,
                          [PIPE_BODY_WIDTH / 2, 1 / 2],
                          [PIPE_BODY_WIDTH, 1],
                          [self.center_x, (GAME_HEIGHT/2 + self.y_bottom/2 + (PIPE_HEAD_HEIGHT/2))],
                          [PIPE_BODY_WIDTH, (GAME_HEIGHT - self.y_bottom - PIPE_HEAD_HEIGHT)])

    def update_position(self):
        self.center_x -= self.speed

    def pause(self):
        self.speed = 0


DISTANCE_BETWEEN_PIPES = 209
class PipeCreator:
    def __init__(self):
        self.is_started = False
        self.pipes = []

    def start_pipes(self):
        self.is_started = True
        first_pipe = Pipe(GAME_WIDTH * 2)
        self.pipes.append(first_pipe)

    def draw(self, canvas):
        if self.is_started:
            self.create_and_remove_pipes()
            for pipe in self.pipes:
                pipe.draw(canvas)

    def create_and_remove_pipes(self):
        # When to create a pipe
        if len(self.pipes) <= 2:
            last_pipe = self.pipes[-1]
            new_pipe_pos = last_pipe.center_x + DISTANCE_BETWEEN_PIPES
            new_pipe = Pipe(new_pipe_pos)
            self.pipes.append(new_pipe)
        # When to remove a pipe
        first_pipe = self.pipes[0]
        if first_pipe.center_x < - PIPE_HEAD_WIDTH / 2.0:
            self.pipes.remove(first_pipe)

    def stop(self):
         for pipe in self.pipes:
            pipe.pause()

GAME_WIDTH = 384
GAME_HEIGHT = 448
class Game:
    def __init__(self):
        self.frame = simplegui.create_frame("Flappy Bird", GAME_WIDTH, GAME_HEIGHT)
        self.frame.start()
        self.background = Background()
        self.bird = Bird()
        self.register_handlers()
        self.pipe_creator = PipeCreator()
        self.score = Score()
        self.game_over = False

    def draw(self, canvas):
        self.background.draw(canvas)
        self.bird.draw(canvas)
        self.pipe_creator.draw(canvas)
        self.score.draw_score(canvas)
        self.update_score()
        if self.pipe_creator.pipes:
            nearest_pipe = self.pipe_creator.pipes[0]
            if self.bird.crash(nearest_pipe):
                print "Crash"
                self.game_over = True
                self.bird.kill()
                self.pipe_creator.stop()

    def update_score(self):
        if not self.game_over:
            if self.pipe_creator.pipes:
                first_pipe = self.pipe_creator.pipes[0]
                if first_pipe.center_x + PIPE_HEAD_WIDTH / 2.0 < self.bird.center_x - BIRD_WIDTH / 2.0:
                    if not first_pipe.is_passed:
                        first_pipe.is_passed = True
                        self.score.score_a_point()

    def key_handler(self, key):
        self.bird.flap()
        if not self.pipe_creator.is_started:
            self.pipe_creator.start_pipes()

    def register_handlers(self):
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.key_handler)
        self.frame.add_button('Restart', restart_button_handler)


def restart_button_handler():
    game = Game()

game = Game()
