from pygame import *
import pygame_menu
init()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x,y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 550:
            self.rect.y += self.speed
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_d:
                    player1.boost = True
            if e.type == KEYUP:
                if e.key == K_d:
                    player1.boost = False

    def update2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 550:
            self.rect.y += self.speed
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    player2.boost = True
            if e.type == KEYUP:
                if e.key == K_RIGHT:
                    player2.boost = False

window = display.set_mode((600,600))
bg = (200,255,255)
window.fill(bg)
def game():
    gamerunning = True
    
    fps = 60
    clock = time.Clock()
    player1 = Player('pl.png',20,275,5,25,50)
    player2 = Player('pl.png',560,275,5,25,50)
    ball = GameSprite('gh.png',200,200,4,50,50)
    from random import randint
    if randint(1,2) == 1:
        speed_x = ball.speed
        speed_y = ball.speed
    else:
        speed_x = -ball.speed
        speed_y = ball.speed

    ongoing_match = False
    player1.reset()
    player2.reset()
    player1.update1()
    player2.update2()
    ball.reset()
    font.init()
    p1_score = 0
    p2_score = 0
    p1_round = 0
    p2_round = 0
    font1 = font.Font(None,48)
    font3 = font.Font(None,48)
    player1.boost = False
    player2.boost = False
    player1.boosttime = 300
    player2.boosttime = 300
    while gamerunning:
        for e in event.get():
            if e.type == QUIT:
                gamerunning = False
            if e.type == KEYDOWN: 
                if e.key == K_d:
                        player1.boost = True
                if e.key == K_RIGHT:
                        player2.boost = True
                if e.key == K_SPACE:
                    if not ongoing_match:
                        ball.rect.x = 200
                        ball.rect.y = 200
                        if randint(1,2) == 1:
                            speed_x = ball.speed
                            speed_y = ball.speed
                        else:
                            speed_x = -ball.speed
                            speed_y = ball.speed
                        ongoing_match = True
        window.fill(bg)
        if ball.rect.x < 0:
            p1_lost = font1.render('Игрок 1 проиграл!',True,(0,0,0))
            window.blit(p1_lost,(200,200))
            if ongoing_match:
                p2_score += 1
            ongoing_match = False
            score = font1.render('Счёт матча:'+str(p1_score) + ':'+str(p2_score),True,(0,0,0))
            window.blit(score,(200,350))
        if ball.rect.x > 600:
            p2_lost = font1.render('Игрок 2 проиграл!',True,(0,0,0))
            window.blit(p2_lost,(200,200))
            if ongoing_match:
                p1_score += 1
            ongoing_match = False
            
            score = font1.render('Счёт матча:'+str(p1_score) + ':'+str(p2_score),True,(0,0,0))
            window.blit(score,(200,350))

        if player1.boost == True and player1.boosttime > 0:
            player1.boosttime -= 1
            player1.speed = 10
        else:
            player1.speed = 5
            
        if player2.boost == True and player2.boosttime > 0:
            player2.boosttime -= 1
            player2.speed = 10
        else:
            player2.speed = 5
        player1.reset()
        player2.reset()
        player1.update1()
        player2.update2()
        ball.reset()
        if ongoing_match:
            ball.rect.x += speed_x
            ball.rect.y += speed_y
            if sprite.collide_rect(player1, ball) or sprite.collide_rect(player2, ball):
                speed_x *= -1.05
                if sprite.collide_rect(player1, ball):
                    p1_round += 1
                else:
                    p2_round += 1
            round_score = font3.render(str(p1_round) +':'+ str(p2_round),True,(0,0,0))
            window.blit(round_score,(275,25))
            if ball.rect.y > 550 or ball.rect.y < 0:
                speed_y *= -1
        display.update()
        clock.tick(fps)
    
def set_difficulty(value, difficulty):
    # Do the job here !
    pass
menu = pygame_menu.Menu('Добро пожаловать!', 400, 300,theme=pygame_menu.themes.THEME_SOLARIZED)
menu.add.text_input('Ваше имя:', default='Олег')
menu.add.button('Играть', game)

menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Выйти', pygame_menu.events.EXIT)

menu.mainloop(window)

    