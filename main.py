# content from kids can code: http://kidscancode.org/blog/
# used Mr. Cozort as a resource 

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math

# Goals- land 
# Rules- Use right and left keys to move and up arrow to jump; fall off plat and respawn
# Display- Score is found at the top of the screen 

# Feature Goals- screen moves up as player jump - like doodle jump; add new plats

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

# Initialize Pygame
pg.init()
 
# Set up the screen
screen_width, screen_height = 800, 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Pygame Start Button")
 
# Button properties
button_width, button_height = 200, 50
button_x, button_y = (screen_width - button_width) // 2, (screen_height - button_height) // 2
button_color = (0, 255, 0)  # Green color for the button
button_text_color = (255, 255, 255)  # White text color
button_font = pg.font.Font(None, 36)
button_text = button_font.render("Start", True, button_text_color)

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # create a group for all sprites
        self.bgimage = pg.image.load(os.path.join(img_folder, 'dj_background.png')).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)
    
        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        
        #for p in range(0,3):
            #p = Coins(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 60, 20, "normal")
            #self.all_sprites.add(p)
            #self.all_coins.add(p) 
    
        self.run()

    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH 
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 0
        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5


                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
            if hits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                print("ouch")
                self.player.hitpoints -= 100 
                if self.player.hitpoints < 1:
                    self.player = pg.quit
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
        # move screen upward when player reaches the top
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.all_platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
# respawns the sprite to the start again
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)          
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.all_platforms) == 0:
            self.playing = False
# spawns in new platforms while moving up
        while len(self.all_platforms) < 6:
            width = random.randrange(50,100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20, "moving")
            self.all_platforms.add(p)
            self.all_sprites.add(p)
                    

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(GREEN)
        self.screen.blit(self.bgimage,(0,0))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        # self.draw_text("Hitpoints: " + str(self.player.hitpoints), 22, BLACK, WIDTH/2, HEIGHT/10)
        self.draw_text("Score: " + str(self.score), 22, BLACK, WIDTH/2, HEIGHT/7)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()

