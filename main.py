# untitled_space_game_
# by Brady Nichols and Mary Serviss
# Music - Brady Nichols
# Art - Mary Serviss

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import time

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.init()
        pg.mixer.init()
        self.BackGround = Background(r'.\img\background.png', [0,0])
        self.TitleScreen = Background(r'.\img\title.png', [0,0])
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.snd_dir = path.join(self.dir, 'snd')

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self) #the self makes it know about the game / have the game variables
        self.all_sprites.add(self.player)

        # Generate main platforms in beginning
        mainplat = Platform(0, HEIGHT-40, WIDTH/2, 40)
        self.all_sprites.add(mainplat)
        self.platforms.add(mainplat)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        
        # Load overworld 1
        pg.mixer.music.load(path.join(self.snd_dir, 'overworld1.mp3'))
        self.run()

    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def show_end_screen(self):
        # End screen
        pg.mixer.music.load(path.join(self.snd_dir, 'victorious.mp3'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill([0, 0, 0])
        self.draw_text("Thank you for playing!", 22, GOLD, WIDTH / 2, HEIGHT / 3)
        self.draw_text("by Brady Nichols and Mary Serviss", 22, GOLD, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("github.com/bradynichols/untitled_space_game", 22, GOLD, WIDTH / 2, HEIGHT * 6/7)
        pg.display.flip()
        # Sleep until music is done, then quit.
        time.sleep(21)
        self.running = False
        self.playing = False

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        
        # Check score for music / screen changes
        if self.score == 500:
            pg.mixer.music.load(path.join(self.snd_dir, 'overworld2.mp3'))
            pg.mixer.music.play(loops=-1)
        
        if self.score == 1000:
            pg.mixer.music.load(path.join(self.snd_dir, 'overworld3.mp3'))
            pg.mixer.music.play(loops=-1)
        
        if self.score == 1500:
            self.show_end_screen()

        # Check if player hits platform
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0

        # Scroll right
        if self.player.rect.x  >= WIDTH * (2/3):
            if self.player.vel.x > 0.05:
                self.player.pos.x -= self.player.vel.x
                for plat in self.platforms:
                    plat.rect.x -= self.player.vel.x
                    if plat.rect.x + plat.image.get_width() <= 0:
                        plat.kill()
                        self.score += 10
                    if plat.rect.top <= 0:
                        plat.kill()

        # Procedurally generate new platforms to keep same average number
        while len(self.platforms) < 9:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(WIDTH, WIDTH+40),
                        random.randrange(HEIGHT/2, HEIGHT),
                        width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

        # Die!
        if self.player.rect.bottom > HEIGHT:
            self.playing = False

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_UP:
                    self.score += 500

    def draw(self):
        # Game loop - draw
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.BackGround.image, self.BackGround.rect)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'maintitle.mp3'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.TitleScreen.image, self.TitleScreen.rect)
        self.draw_text("By Brady Nichols and Mary Serviss", 22, GOLD, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press a key to play", 22, GOLD, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, GOLD, WIDTH / 2, int(HEIGHT * 7/8))
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        time.sleep(2)
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen() # game over

pg.quit()