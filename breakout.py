from operator import truediv
import pygame
pygame.init()

#Scren parameters
screen_width = 600
screen_height = 600

#Initializing Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.update()
start_game = 0

#Title and Icon
pygame.display.set_caption("Breakout")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#Colors
Font_Color = (0, 255, 255)
Game_over_color = (255, 0, 255)
Black_Screen = (0, 0, 0)
Background_Color = (200, 200, 200)
Brick_Color = (120, 0, 0)
Paddle_Color = (0, 0, 250)
Ball_Color = (0, 0, 250)
Border_Color = (0, 0, 0)

#Paddle
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = (screen_width - self.width) / 2
        self.y = screen_height - 50
        self.change_X = 0
        self.paddle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def move_paddle(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_X = -0.5
            
            if event.key == pygame.K_RIGHT:
                self.change_X = +0.5
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.change_X = 0.0

        self.x += self.change_X
        if self.x < 0:
            self.x = 0
        elif self.x >= screen_width - self.width:
            self.x = screen_width - self.width
        
    def draw_paddle(self):
        self.paddle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, Paddle_Color, self.paddle_rect)
        pygame.draw.rect(screen, Border_Color, self.paddle_rect, 2)
            


#Bricks Wall
bricks = []
class wall():
    def __init__(self):
        self.rows = 6
        self.cols = 6
        self.width = screen_width // self.cols
        self.height = 35

    def create_wall(self):
        global bricks
        bricks = []
        individual_brick = []
        for row in range(self.rows):
            brick_row = []
            for col in range(self.cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                individual_brick = [rect]
                brick_row.append(individual_brick)
            bricks.append(brick_row)


    def draw_wall(self):
        for row in bricks:
            for block in row:
                pygame.draw.rect(screen, Brick_Color, block[0])
                pygame.draw.rect(screen, Background_Color, (block[0]), 2)

#Game over Variable
game_over_ = False

#Game Winning variable
game_won_ = False

#Ball
class Ball:
    def __init__(self):
        self.paddle_ = Paddle()
        self.x = screen_width / 2
        self.y = screen_height / 2 + 100
        self.speed_x = 0.15
        self.speed_y = 0.1
        self.game_over = 5
        self.game_won = 1
        self.ball_rect = pygame.Rect(self.x, self.y, 15, 15)
        self.collision_margin = 5

    def draw_ball(self):
        self.ball_rect = pygame.Rect(self.x, self.y, 15, 15)
        pygame.draw.rect(screen, Ball_Color, self.ball_rect)
        pygame.draw.rect(screen, Border_Color, self.ball_rect, 2)

    def move_ball(self):
        self.paddle_.draw_paddle()
        self.paddle_.move_paddle()
        
        #Collision Checks
        self.game_won = 1
        row_count = 0
        for row in bricks:
            brick_count = 0
            for brick in row:
                if self.ball_rect.colliderect(brick[0]):
                    if abs(self.ball_rect.bottom - brick[0].top) < self.collision_margin:
                        self.speed_y *= -1
                    if abs(self.ball_rect.top - brick[0].bottom) < self.collision_margin:
                        self.speed_y *= -1
                    if abs(self.ball_rect.right - brick[0].left) < self.collision_margin:
                        self.speed_x *= -1
                    if abs(self.ball_rect.left - brick[0].right) < self.collision_margin:
                        self.speed_x *= -1
                    bricks[row_count][brick_count][0] = (0, 0, 0, 0)
                if bricks[row_count][brick_count][0] != (0, 0, 0, 0):
                    self.game_won = 0
                brick_count += 1
            row_count += 1

        if self.x >= screen_width - 15 or self.x <= 0:
            self.speed_x *= -1
        
        if self.y <= 0:
            self.speed_y *= -1

        if self.y >= screen_width - 15:
            self.x = screen_width / 2
            self.y = screen_height / 2 + 100
            self.speed_y *= -1
            self.game_over -= 1
    
        if self.ball_rect.colliderect(self.paddle_.paddle_rect):
            if abs(self.ball_rect.bottom - self.paddle_.paddle_rect.top) < self.collision_margin and self.x > 0:
                self.speed_y *= -1
            if abs(self.ball_rect.right - self.paddle_.paddle_rect.left) < self.collision_margin:
                self.speed_x *= -1
            if abs(self.ball_rect.left - self.paddle_.paddle_rect.right) < self.collision_margin:
                self.speed_x *= -1

        self.x += self.speed_x
        self.y -= self.speed_y

        #Game Ending checks
        if self.game_over == 0:
            global game_over_
            game_over_ = True

        if self.game_won == 1:
            global game_won_
            game_won_ = True

        

#Objects
bricks_ = wall()
bricks_.create_wall()
ball = Ball()

#Game Loop
open = True
while open:
    if start_game == 0:
        screen.fill(Black_Screen)
        message1 = "Assalam u Alaikum"
        message2 = "Welcome to Breakout!"
        message3 = "Press SPACE to start the game."
        font = pygame.font.Font(None, 30)
        show_message1 = font.render(message1, True, Font_Color)
        show_message2 = font.render(message2, True, Font_Color)
        show_message3 = font.render(message3, True, Font_Color)
        screen.blit(show_message1, [screen_width / 2 - 150, screen_height / 2 - 50])
        screen.blit(show_message2, [screen_width / 2 - 150, screen_height / 2])
        screen.blit(show_message3, [screen_width / 2 - 150, screen_height / 2 + 70])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game = 1
            
            if event.type == pygame.QUIT:
                open = False

    if start_game == 1:
        screen.fill(Background_Color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                open = False

        bricks_.draw_wall()
        ball.draw_ball()
        ball.move_ball()

        while game_over_ == True:
            screen.fill(Black_Screen)
            msg = "You Lost the game."
            font = pygame.font.Font(None, 30)
            Game_over_msg = font.render(msg, True, Game_over_color)
            screen.blit(Game_over_msg, [screen_width / 2 - 100, screen_height / 2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    open = False
                    break
            break

        while game_won_ == True:
            screen.fill(Black_Screen)
            msg_ = "You Won the game."
            font = pygame.font.Font(None, 30)
            Game_won_msg = font.render(msg_, True, Game_over_color)
            screen.blit(Game_won_msg, [screen_width / 2 - 100, screen_height / 2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    open = False
                    break
            break

        pygame.display.update()

