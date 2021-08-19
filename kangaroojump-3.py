''' 
init semuanya
animasi kanggoroo loncat 
animasi pijakan 
gesekan antara kanggoro dengan pijakan
pijakan yang broken
score, high score 
tampilan awal tampilan game over


'''


import pygame
from pygame.locals import *
import sys
import random

class KangarooJump:
    def __init__(self): #inisialisasi semua 
        self.screen = pygame.display.set_mode((400, 700)) #set ukuran window game 
        pygame.display.set_caption("Kangaroo Jump") #set window title
        self.bg = pygame.image.load('assets/bg-start.png').convert_alpha()
        self.init_surface = pygame.image.load('assets/start-ok.png').convert_alpha()
        self.bg_surface = pygame.image.load('assets/bg-start.png').convert_alpha()
        self.ground_1 = pygame.image.load("assets/pijakan-05.png").convert_alpha()
        pygame.font.init() #init font nya 
        self.score = 0 
        self.high_score = 0
        self.font = pygame.font.Font("assets/GAMERIA.ttf", 25) #font yang dipakai 
        #load semua aset 
        self.ground_fly = pygame.image.load("assets/pijakan-03.png").convert_alpha()
        self.ground_broken1 = pygame.image.load("assets/pijakan-patah-1.png").convert_alpha()
        self.ground_broken2 = pygame.image.load("assets/pijakan-patah-2.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/kangaroo-3.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/kangaroo-right.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/kangaroo-4.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/kangaroo-left.png").convert_alpha()
        self.kangarooOver = pygame.image.load("assets/kangaroo_over.png").convert_alpha()
        self.spring = pygame.image.load("assets/spring.png").convert_alpha() #peer atau bonus loncat dengan cepat
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()
        pygame.mixer.init() #untuk sound
        self.jump_sound = pygame.mixer.Sound("sound/Jump33.wav")
        self.spring_sound = pygame.mixer.Sound("sound/Jump40.wav")
        self.direction = 0
        self.playerx = 200
        self.playery = 300
        self.platforms = [[200, 250, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.kangaroo_movement = 0
        self.score_surface = 0
        self.score_rect = 0
        self.high_score_surface = 0
        self.high_score_rect = 0
        self.game_font = pygame.font.Font("assets/GAMERIA.ttf", 25)
        self.scoredisplay= False
        self.running = True
            
    def updatePlayer(self): #update kangaroo untuk jump
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 0.5
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 0.5
        
        key = pygame.key.get_pressed() #ketika key di pencet (kanan dan kiri)
    
        if key[K_RIGHT]: #pencet keyboard panah kanan 
            if self.kangaroo_movement < 10:
                self.kangaroo_movement += 1 
            self.direction = 0

        elif key[K_LEFT]: #pencet keyboard panah kiri
            if self.kangaroo_movement > -10:
                self.kangaroo_movement -= 1
            self.direction = 1
        else:
            if self.kangaroo_movement > 0:
                self.kangaroo_movement -= 1
            elif self.kangaroo_movement < 0:
                self.kangaroo_movement += 1
        if self.playerx > 400:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 400
        self.playerx += self.kangaroo_movement
        if self.playery - self.cameray <= 200: #akan menampilkan kangguru berada dimana
            self.cameray -= 10
            
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))
                    
    def updatePlatforms(self): 
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.ground_1.get_width() - 20, self.ground_1.get_height())
            #untuk kangaroo ke kanan dan kiri 
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 20, self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2: #jika playaer tdk ketemu dengan platfom 2 maka dia akan loncat 
                    self.jump = 15
                    self.jump_sound.play()
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 500: #yang gerak kanan kiri
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 700:
                platform = random.randint(0, 700)
                if platform < 250:
                    platform = 0
                elif platform < 500:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 500), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 500)
                if check > 400 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
     
            if p[2] == 0:
                self.screen.blit(self.ground_1, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.ground_fly, (p[0], p[1] - self.cameray))
                
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.ground_broken1, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.ground_broken2, (p[0], p[1] - self.cameray))
                
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                self.jump = 30
                self.cameray -= 30
                self.spring_sound.play()
                
    def generatePlatforms(self):
        on = 700
        while on > -200:
            x = random.randint(0,700)
            platform = random.randint(0, 400)
            if platform < 500:
                platform = 0
            elif platform > 500:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 700))    
    
    def score_display(self):        
            if self.scoredisplay:
                self.score_surface = self.game_font.render(str(int(self.score)),True,(255,255,255))
                self.score_rect = self.score_surface.get_rect(center = (200,30))
                self.screen.blit(self.score_surface,self.score_rect)
            else:
                self.score_surface = self.game_font.render(f'Score {int(self.score)}' ,True,(255,255,255))
                self.score_rect = self.score_surface.get_rect(center = (200,30))
                self.screen.blit(self.score_surface,self.score_rect)

                self.high_score_surface = self.game_font.render(f'High score {int(self.high_score)}',True,(255,255,255))
                self.high_score_rect = self.high_score_surface.get_rect(center = (195,600))
                self.screen.blit(self.high_score_surface,self.high_score_rect)       
                
            
    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill((255,192,203))
        self.draw_text("GAME OVER", 48, (255, 255, 255), 400 / 2, 400 / 4)
        self.screen.blit(self.kangarooOver,(100,200))
        self.score_display()
        self.draw_text("Press a key to play again", 22, (255, 255, 255),400 / 2, 700 * 3 / 4)
        if self.score > self.high_score:
            self.high_score = self.score
            self.draw_text("NEW HIGH SCORE", 22, (255, 255, 255), 400 / 2, 800 / 2 + 40)

        else:
            self.score_display()
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # jika window close tanda x di click
                pygame.quit() #keluar
                sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.new()
        
    def new(self):
        # start a new game
        pygame.mixer.music.load('sound/Happy Tune.ogg')
        self.cameray = 0
        self.score = 0
        self.springs = []
        self.platforms = [[200, 250, 0, 0]]
        self.generatePlatforms()
        self.playerx = 200
        self.playery = 300
        self.run()
        
    def run(self):
        pygame.mixer.music.play(loops=-1)
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255,255,255))
            self.screen.blit(self.bg_surface,(0,0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # jika window close tanda x di click
                    pygame.quit() #keluar
                    sys.exit()

            if self.playery - self.cameray > 600: #jika kangaro lebih dari 600
                return self.show_go_screen()

            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (180, 25)) #untuk display score     
            pygame.display.flip()
            
                       
    def start(self):
        pygame.mixer.music.load('sound/Yippee.ogg')
        pygame.mixer.music.play(loops=-1)
        self.screen.fill((255,192,203))
        self.screen.blit(self.init_surface, (0, 0))
        # self.score_display()
        pygame.display.flip()
        self.wait_for_key()
        self.start_sound.fadeout(300)
        
        
    def wait_for_key(self):
        clock = pygame.time.Clock()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # jika window close tanda x di click
                    pygame.quit() #keluar
                    sys.exit()
                    waiting = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.new()
                        
    def draw_text(self, text, size, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect) 
        
# KangarooJump().start()
k = KangarooJump()
k.start()
while k.runing:
    k.new()
    k.show_go_screen()

pygame.quit()
