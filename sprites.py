import pygame as pg
import sys
import os
import argparse

from pygame.constants import K_DOWN, K_KP2, K_KP4, K_KP6, K_KP8, K_LEFT, K_RIGHT, K_UP, KEYDOWN, KEYUP
from pygame.surface import Surface
import spritesdict as spd

class chr_bg(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image:Surface = pg.image.load(os.path.join("assets", "background2.png")).convert_alpha()
        #bg_width, bg_height = self.image.get_width(), self.image.get_height()
        self.rect:pg.Rect = screen.blit(self.image, (0, 0))

class chr_out(pg.sprite.Sprite):
    def __init__(self, chr:str, clr:str, dir:str):
        super().__init__()
        if chr in spd.sprites_dict and clr in spd.sprites_dict[chr]:
            self.all_sprites = {}
            self.sprites_dict = spd.sprites_dict[chr]
            self.sprites_ext = self.sprites_dict["base_ext"]
            self.sprites_image = os.path.join(spd.sprites_dict["base_path"], self.sprites_dict["folder"], self.sprites_dict["base_name"])
            keys:list = ["down", "up", "right"]

            for key in keys:
                self.sprites = []
                self.sprites_left = []
                for img in self.sprites_dict[clr][key]:
                    tmp_sprite = pg.image.load(self.sprites_image+img+self.sprites_ext).convert_alpha()
                    if key == "right":
                        self.sprites_left.append(pg.transform.flip(tmp_sprite, True, False))
                    self.sprites.append(tmp_sprite)
                self.all_sprites[key] = self.sprites.copy()
                if key == "right":
                    self.all_sprites["left"] = self.sprites_left.copy()

            self.sprite_direction = dir
            self.start_animation = chr_autorun
            self.current_sprite = 0
            self.image:Surface = self.all_sprites[dir][self.current_sprite]
            self.rect:pg.Rect = self.image.get_rect()
            self.rect.center = screen.get_rect().center
        else:
            print("Sprites '" + chr + " " + clr + "' not found")

    def goDirection(self, dir):
        self.sprite_direction = dir
        self.start_animation = True

    def stop(self):
        if chr_autorun == False:
            self.start_animation = False

    def update(self,speed):
        if self.start_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.start_animation == chr_autorun
        self.image = self.all_sprites[self.sprite_direction][int(self.current_sprite)]

screen_width = 640
screen_height = 480
fps = 60
title = "CR SPRITES ANIMATE"
parser = argparse.ArgumentParser(description='Animate CR characters from sprites')
parser.add_argument("character", help="Selects the character to animate")
parser.add_argument("-a", "--autorun", help="Autorun character", action="store_true")
parser.add_argument("-r", "--red", help="Red version character", action="store_true")
chr_arg = parser.parse_args().character
chr_autorun = parser.parse_args().autorun
chr_color = "red" if parser.parse_args().red else "blue"

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption(title)
#rectScr = screen.get_rect()

# Creating the sprites and groups
group_sprites = pg.sprite.Group()
chr = chr_out(chr_arg, chr_color, "down")
bg = chr_bg()
group_sprites.add(bg, chr)

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT: 
            pg.quit()
            sys.exit(0)
        if event.type == KEYUP:
            chr.stop()
        if event.type == KEYDOWN:
            if (event.key == K_DOWN or event.key == K_KP2):
                chr.goDirection("down")
            elif (event.key == K_UP or event.key == K_KP8):
                chr.goDirection("up")
            elif (event.key == K_RIGHT or event.key == K_KP6):
                chr.goDirection("right")
            elif (event.key == K_LEFT or event.key == K_KP4):
                chr.goDirection("left")

    #screen.fill((255,255,255)) #blanc
    screen.fill((0,0,0)) #noir
    group_sprites.draw(screen)
    group_sprites.update(0.20)
    pg.display.flip()
    time = clock.tick(fps)
    pg.display.update()