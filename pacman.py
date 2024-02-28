import pygame
from board import boards
import math

pygame.init()
pygame.font.init()

# SETTINGS OF THE GAME CONSTANTS
WIDTH = 900
HEIGHT = 950
PI = math.pi  # used to make the arc of the board
fps = 60
font = pygame.font.SysFont('freesansbold.ttf',30)

# SETTING THE GAME VARAIBLES
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
level = boards  # this variable for now only loads one single level, but can hold more
color = 'blue'  # the color of the level can be changed and vary on the level

# sets the images that consists the player, so u can have the animation of the pac-man
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

#sets the images of the ghosts
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45,45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45,45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45,45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45,45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45,45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45,45))

#ghost sets
blinky_x = 56
blinky_y = 58
blinky_direction = 0

pinky_x = 440
pinky_y = 378
pinky_direction = 2

inky_x = 470
inky_y = 378
inky_direction = 2

clyde_x = 455
clyde_y = 378
clyde_direction = 2

# initial set of where the player starts, can cary on lvl as well
player_x = 450
player_y = 663
player_speed = 2
player_score = 0
powerup = 0
scorer = 1
counter_add = 1
lives = 3

# both flicker and counter are used to determine the update the position of the player, ass well as the power ups on the
# screen
counter = 0
flicker = False

# creates the variables that gonna be used to determine the player movimentation on the board
direction = 0
turns_allowed = [False, False, False, False]
direction_command = 0
timer_event = pygame.USEREVENT+1

#ghosts varaibles
ghosts_eatens = [False, False, False, False]
targets = [(player_x, player_y),(player_x, player_y),(player_x, player_y),(player_x, player_y)]
ghost_speed = 2

blinky_dead = False
pinky_dead = False
inky_dead = False
clyde_dead = False

blinky_box = False
pinky_box = False
inky_box = False
clyde_box = False


class Ghost:
    def __init__(self, x_cord, y_cord, target, speed, image, direction, dead, box, id):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.target = target
        self.speed = speed
        self.image = image
        self.direction = direction
        self.dead = dead
        self.box = box
        self.id = id

        self.center_x = self.x_cord + 22
        self.center_y = self.y_cord + 22
        self.turns, self.box = self.check_collisions()
        self.rect = self.draw()

    def check_collisions(self):

        num1 = ((HEIGHT-50)//32)
        num2 = (WIDTH//30)
        num3 = 15

        self.turns = [False, False, False, False]

        if self.center_x // 30 < 29:
            if level[self.center_y//num1][(self.center_x - num3)//num2] < 3 \
                or (level[self.center_y//num1][(self.center_x - num3)//num2] == 9 and (
                self.box or self.dead)):
                    self.turns[1] = True
            if level[self.center_y//num1][(self.center_x + num3)//num2] < 3 \
                or (level[self.center_y//num1][(self.center_x + num3)//num2] == 9 and (
                self.box or self.dead)):
                    self.turns[0] = True

            if level[(self.center_y + num3)//num1][self.center_x//num2] < 3 \
                or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 and (
                self.box or self.dead)):
                    self.turns[3] = True
            if level[(self.center_y - num3)//num1][self.center_x//num2] < 3 \
                or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 and (
                self.box or self.dead)):
                    self.turns[2] = True

        if self.direction == 2 or self.direction == 3:
            if 10 <= self.center_x % num2 <= 20:
                if level[(self.center_y + num1)//num1][self.center_x//num2] < 3 \
                    or (level[(self.center_y + num1)//num1][self.center_x//num2] == 9
                        and self.box and self.dead):
                        self.turns[3] = True
                if level[(self.center_y - num1)//num1][self.center_x//num2] < 3 \
                    or (level[(self.center_y - num1)//num1][self.center_x//num2] == 9
                        and self.box and self.dead):
                        self.turns[2] = True

            if 10 <= self.center_y % num1 <= 20:

                if level[self.center_y//num1][(self.center_x + num2)//num2] < 3 \
                    or (level[self.center_y//num1][(self.center_x + num2)//num2] == 9 and
                        self.box and self.dead):
                        self.turns[0] = True

                if level[self.center_y//num1][(self.center_x - num2)//num2] < 3 \
                    or (level[self.center_y//num1][(self.center_x - num2)//num2] == 9 and
                        self.box and self.dead):
                        self.turns[1] = True

        if self.direction == 0 or self.direction == 1:
            if 10 <= self.center_x % num2 <= 20:
                if level[(self.center_y + num3)//num1][self.center_x//num2] < 3 \
                    or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9
                        and self.box and self.dead):
                        self.turns[3] = True
                if level[(self.center_y - num3)//num1][self.center_x//num2] < 3 \
                    or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9
                        and self.box and self.dead):
                        self.turns[2] = True

            if 10 <= self.center_y % num1 <= 20:

                if level[self.center_y//num1][(self.center_x + num3)//num2] < 3 \
                    or (level[self.center_y//num1][(self.center_x + num3)//num2] == 9 and
                        self.box and self.dead):
                        self.turns[0] = True

                if level[self.center_y//num1][(self.center_x - num3)//num2] < 3 \
                    or (level[self.center_y//num1][(self.center_x - num3)//num2] == 9 and
                        self.box and self.dead):
                        self.turns[1] = True


        else:
            self.turns[0] = True
            self.turns[1] = True

        if 350 < self.x_cord < 550 and 370 < self.y_cord < 490:
            self.box = True
        else:
            self.box = False


        return self.turns, self.box

    def draw(self):

        if (not self.dead and not powerup) or (ghosts_eatens[self.id] and powerup and not self.dead):
            screen.blit(self.image, (self.x_cord, self.y_cord))
        elif powerup and not self.dead or not (ghosts_eatens[self.id]):
            screen.blit(spooked_img, (self.x_cord, self.y_cord))
        else:
            screen.blit(dead_img, (self.x_cord, self.y_cord))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36,36))

        return ghost_rect


    def move_clyde(self):

        if self.direction == 0:
            if self.target[0] > self.x_cord and self.turns[0]:
                self.x_cord += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_cord and self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed

                elif self.target[1] < self.y_cord and self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed

                elif self.target[0] < self.x_cord and self.turns[1]:
                    self.direction = 1
                    self.x_cord -= self.speed

                elif self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed

                elif self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed

                elif self.turns[1]:
                    self.direction = 1
                    self.x_cord += self.speed

            elif self.turns[0]:
                if self.target[1] > self.y_cord and self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed
                if self.target[1] > self.y_cord and self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed
                else:
                    self.x_cord -= self.speed
        if self.direction == 1:
            if self.target[1] > self.y_cord and self.turns[3]:
                self.direction = 3
                self.y_cord += self.speed
            elif self.target[0] < self.x_cord and self.turns[1]:
                self.x_cord -= self.speed

            elif not self.turns[1]:
                if self.target[1] > self.y_cord and self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed

                elif self.target[1] < self.y_cord and self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed

                elif self.target[0] < self.x_cord and self.turns[0]:
                    self.direction = 0
                    self.x_cord += self.speed

                elif self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed

                elif self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed

                elif self.turns[0]:
                    self.direction = 0
                    self.x_cord -= self.speed

            elif self.turns[1]:
                if self.target[1] > self.y_cord and self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed
                if self.target[1] > self.y_cord and self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed
                else:
                    self.x_cord += self.speed
        if self.direction == 2:
            if self.target[0] < self.x_cord and self.turns[0]:
                self.direction = 0
                self.x_cord -= self.speed
            elif self.target[1] < self.y_cord and self.turns[2]:
                self.direction = 2
                self.y_cord -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.y_cord and self.turns[0]:
                    self.direction = 0
                    self.x_cord -= self.speed

                elif self.target[1] < self.y_cord and self.turns[1]:
                    self.direction = 1
                    self.x_cord += self.speed

                elif self.target[1] > self.y_cord and self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed

                elif self.turns[3]:
                    self.direction = 3
                    self.y_cord += self.speed

                elif self.turns[1]:
                    self.direction = 1
                    self.x_cord += self.speed

                elif self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_cord -= self.speed

            elif self.turns[2]:
                if self.target[0] > self.y_cord and self.turns[0]:
                    self.direction = 0
                    self.x_cord -= self.speed
                if self.target[0] > self.y_cord and self.turns[1]:
                    self.direction = 1
                    self.x_cord += self.speed
                else:
                    self.y_cord -= self.speed
        if self.direction == 3:
            if self.target[1] < self.y_cord and self.turns[3]:
                self.direction = 3
                self.y_cord += self.speed
            elif not self.turns[3]:
                if self.target[0] < self.x_cord and self.turns[0]:
                    self.direction = 0
                    self.x_cord -= self.speed
                elif self.target[0] < self.x_cord and self.turns[1]:
                    self.direction = 1
                    self.x_cord += self.speed
                elif self.target[1] < self.y_cord and self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_cord -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_cord += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_cord -= self.speed
                elif self.turns[3]:
                    self.direction =3
                    self.y_cord += self.y_cord


            elif self.turns[2]:
                if self.target[0] > self.y_cord and self.turns[0]:
                    self.direction = 0
                    self.x_cord -= self.speed
                if self.target[0] > self.y_cord and self.turns[1]:
                    self.direction = 1
                    self.x_cord += self.speed
                else:
                    self.y_cord -= self.speed

        if self.x_cord < -30:
            self.x_cord = 900
        elif self.x_cord > 900:
            self.x_cord = -30

        return self.x_cord, self.y_cord, self.direction

def draw_board(lvl):
    """
    :param lvl:
    :return:

    This function receives the wanted lvl as parameter and renders it in the screen
    The level model is a tile based matrix, that depend on the number identifies a certain object in the map
    0 - empty space
    1 - fruit
    2 - superpower
    9 - ghostgate
    3 <= 8 - map wall
    """
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)

    for i in range(len(lvl)):
        for j in range(len(lvl[i])):

            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', ((j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1))), 4)

            elif lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', ((j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1))), 10)

            elif lvl[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + 0.5 * num2, i * num1),
                                 (j * num2 + 0.5 * num2, i * num1 + num1), 3)

            elif lvl[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + 0.5 * num1),
                                 (j * num2 + num2, i * num1 + 0.5 * num1), 3)

            elif lvl[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - 0.5 * num2), (i * num1 + 0.5 * num1), num2, num1], 0,
                                PI / 2, 3)

            elif lvl[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + 0.5 * num2), (i * num1 + 0.5 * num1), num2, num1], PI / 2,
                                PI, 3)

            elif lvl[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + 0.5 * num2), (i * num1 - 0.5 * num1), num2, num1], PI,
                                1.5 * PI, 3)

            elif lvl[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - 0.5 * num2), (i * num1 - 0.5 * num1), num2, num1], 1.5 * PI,
                                0, 3)

            elif lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + 0.5 * num1),
                                 (j * num2 + num2, i * num1 + 0.5 * num1), 3)

def draw_player():
    """
    :return:
    This function draws the player on the screen, and rotates it so its looks exactly where it is going
    """
    # 0-right, 1-left, 2-up 3-down
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    if direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    if direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    if direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    """
    :param centerx:
    :param centery:
    :return turns: list
    This function verifies if the position that is required to go is available to the player goes to
    , or not (ex: a wall)
    """
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15  # fudge factor

    # check collisions based on center_x and center_y of the player + fudge factor

    if centerx // 30 < 29:  # it is in the board

        if direction == 0:  # verifies if it can go back, from what it came from
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:  # verifies if it can change the direction, to got to another place

            if 10 <= centerx % num2 <= 20:  # this is a fudge so you don't verify a faraway tile
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True

            if 10 <= centery % num1 <= 20:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:

            if 10 <= centerx % num2 <= 20:

                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True

            if 10 <= centery % num1 <= 20:

                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True

    else: # trying to reach out the board, must go back
        turns[0] = True
        turns[1] = True

    return turns

def move_player(playx,playy):

    # right, left, up, down - 0, 1, 2, 3

    if direction == 0 and turns_allowed[0]:
        playx += player_speed
    elif direction == 1 and turns_allowed[1]:
        playx -= player_speed
    elif direction == 2 and turns_allowed[2]:
        playy -= player_speed
    elif direction == 3 and turns_allowed[3]:
        playy += player_speed

    return (playx, playy)

def draw_score():
    #self made
    text_score = font.render(f'Score: {player_score}',False, (255,255,255))
    screen.blit(text_score, (15, HEIGHT-30))
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (20,20)),(150 + 25 * i, HEIGHT-30))

def eat_dots(playx, playy):
    #self made
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15

    center_x = playx + 23
    center_y = playy + 24

    new_score = player_score
    if level[center_y//num1][center_x//num2] == 1:
        new_score = player_score + scorer
        level[center_y//num1][center_x//num2] = 0
    return new_score

def eat_powerup(playx, playy, powerup):
    #self made
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15

    center_x = playx + 23
    center_y = playy + 24

    if level[center_y//num1][center_x//num2] == 2:
        level[center_y//num1][center_x//num2] = 0

        # player_speed = 4
        # scorer = 4
        pygame.time.set_timer(timer_event, 5000)

        return 1
    else:
        return powerup



run = True

while run:
    timer.tick(fps)

    if counter < 19:
        counter += counter_add

        if counter > 3:
            flicker = False

    else:
        counter = 0
        flicker = True

    screen.fill('black')
    draw_board(level)
    draw_player()
    draw_score()

    blinky = Ghost(blinky_x, blinky_y, targets[0], 2, blinky_img, blinky_direction, 0, blinky_box,0)
    pinky = Ghost(pinky_x, pinky_y, targets[2], 2, pinky_img, pinky_direction, 0, pinky_box,2)
    inky = Ghost(inky_x, inky_y, targets[1], 2, inky_img, inky_direction, 0, inky_box,1)
    clyde = Ghost(clyde_x, clyde_y, targets[0], 2, clyde_img, clyde_direction, 0, clyde_box,0)

    center_x = player_x + 23
    center_y = player_y + 24

    turns_allowed = check_position(center_x, center_y)

    player_x, player_y = move_player(player_x, player_y)

    blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
    pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
    inky_x, inky_y, inky_direction = inky.move_clyde()
    clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

    player_score = eat_dots(player_x, player_y)
    powerup = eat_powerup(player_x, player_y, powerup)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == timer_event:
            powerup = 0
            player_speed = 2
            scorer = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    if player_x > 900:
        player_x -= 47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()

pygame.quit()
