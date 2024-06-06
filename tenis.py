import pygame
import sys
import time

from pygame.locals import *

class sidePR:
    def __init__(self):
        self.xp = 470
        self.yp = 0

class sideP:
    def __init__(self):
        self.x = 0
        self.y = 0

class port1:
    def __init__(self, surface, change):
        self.change = change
        self.surface = surface
        self.port = pygame.Rect(self.change.x, self.change.y, 30, 150)
    
    def draw(self):
        self.port.topleft = (self.change.x, self.change.y)   
        pygame.draw.rect(self.surface, (255, 0, 0), self.port)

class port2:
    def __init__(self, surface, change):
        self.change = change
        self.surface = surface
        self.port = pygame.Rect(self.change.xp, self.change.yp, 30, 150)
    
    def draw(self):
        self.port.topleft = (self.change.xp, self.change.yp)   
        pygame.draw.rect(self.surface, (255, 0, 0), self.port)

class ball:
    def __init__(self, surface, change_p, change_r):
        self.change_p = change_p
        self.change_r = change_r
        self.surface = surface
        self.xb = 250
        self.yb = 300
        self.radius = 10
        self.dx = 10
        self.dy = 10
        self.port1 = port1(self.surface, self.change_p)
        self.port2 = port2(self.surface, self.change_r)
        self.game_running = True
    
    def draw(self):
        self.surface.fill((0, 0, 0))
        self.port1.draw()
        self.port2.draw()
        pygame.draw.circle(self.surface, (255, 255, 255), (self.xb, self.yb), self.radius)
        pygame.display.flip()
    
    def move(self):
        self.xb += self.dx
        self.yb += self.dy 
        
        # Check for collision with the top and bottom of the screen
        if self.yb <= 0 or self.yb >= 600:
            self.dy = -self.dy
        
        # Check for collision with the paddles
        if self.xb - self.radius <= self.port1.port.right and self.port1.port.top <= self.yb <= self.port1.port.bottom:
            self.dx = -self.dx
        elif self.xb + self.radius >= self.port2.port.left and self.port2.port.top <= self.yb <= self.port2.port.bottom:
            self.dx = -self.dx
        
        # Check for out of bounds (left or right of the screen)
        if self.xb <= 0 or self.xb >= 500:
            self.game_running = False 
        
        self.draw()
    
    def move_up(self):
        if self.change_r.yp > 0:
            self.change_r.yp -= 50
            self.draw()
    
    def move_upl(self):
        if self.change_p.y > 0:
            self.change_p.y -= 50
            self.draw()
    
    def move_down(self):
        if self.change_r.yp < 450:
            self.change_r.yp += 50
            self.draw()
    
    def move_downl(self):
        if self.change_p.y < 450:
            self.change_p.y += 50
            self.draw()

class Game:
    def __init__(self):
        pygame.init()
        
        self.area = pygame.display.set_mode((500, 600))
        
        self.change_p = sideP()
        self.change_r = sidePR()
        self.reset_game()
        
        self.running = True

    def reset_game(self):
        self.area.fill((0, 0, 0))
        self.change_p.y = 0
        self.change_r.yp = 0
        self.ball = ball(self.area, self.change_p, self.change_r)
        self.ball.draw()

    def run(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        font = pygame.font.SysFont(None, 48)  # None means default font, 48 is the font size
        text = font.render('Game Over', True, BLACK)  # True for anti-aliasing
        button_font = pygame.font.SysFont(None, 36)
        restart_text = button_font.render('Restart', True, BLACK)
        button_rect = pygame.Rect(200, 300, 100, 50)

        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if self.ball.game_running:
                        if event.key == K_TAB:
                            self.ball.move()
                        elif event.key == K_UP:
                            self.ball.move_up()
                        elif event.key == K_w:
                            self.ball.move_upl()
                        elif event.key == K_DOWN:
                            self.ball.move_down()
                        elif event.key == K_s:
                            self.ball.move_downl()
                elif event.type == MOUSEBUTTONDOWN:
                    if not self.ball.game_running and button_rect.collidepoint(event.pos):
                        self.reset_game()
                elif event.type == QUIT:
                    self.running = False
            
            if not self.ball.game_running:
                self.area.fill(WHITE)
                self.area.blit(text, (150, 200))
                pygame.draw.rect(self.area, (200, 200, 200), button_rect)
                self.area.blit(restart_text, (210, 310))
                pygame.display.flip()
            else:
                self.ball.move()
                time.sleep(0.1)

if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
e