import pygame, sys,random,pickle 

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules

pygame.init() # initiate pygame

WINDOW_SIZE = (1920,1080)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

R_WINDOW_SIZE = [1920,1080] # set up window size

display = pygame.Surface(R_WINDOW_SIZE)
global img_S
img_S = 2

def outline(img,loc,color):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    mask_surf = pygame.Surface(img.get_size())
    for pixel in mask_outline:
        mask_surf.set_at(pixel,color)
    mask_surf.set_colorkey((0,0,0))
    display.blit(mask_surf,(loc[0]-1,loc[1]))
    display.blit(mask_surf,(loc[0]+1,loc[1]))
    display.blit(mask_surf,(loc[0],loc[1]-1))
    display.blit(mask_surf,(loc[0],loc[1]+1))

global animation_frames

animation_frames = {} # 이미지 파일 이름에 따른 이미지(pygame.image.load)형태로 저장


def load_animation(path, frame_durations,trans):
    global animation_frames
    global img_S
    animation_name = path.split("/")[-1] #애니메이션 파일 명을 애니메이션 사진 파일의 기본이름으로 설정
    animation_frame_data = []

    n = 0
    for frame in frame_durations:# 접근성 강화 -> 애니매이션 양산 가능
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"

        animation_image = pygame.image.load((img_loc)).convert_alpha()
        animation_image = pygame.transform.scale(animation_image,(animation_image.get_width()*img_S, animation_image.get_height()*img_S))
        animation_image = pygame.transform.scale(animation_image, (animation_image.get_width()*trans[0], animation_image.get_height()*trans[1]))
        animation_image.set_colorkey((255,255,255))

        animation_frames[animation_frame_id] = animation_image.copy()

        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1

    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value: #기존 액션 동작이 새 동작과 다른 경우
        action_var = new_value #기존 액션 동작을 새 액션 동작으로 바꿈
        frame = 0 #해당 동작의 이미지 프레임을 0으로 설정(초기화)
    return action_var, frame

class Player:
    def __init__(self,pos,right_k,left_k,jump_k,attack_k,weapon_k,dash_k,color):
        global img_S

        self.image_width = 32
        self.image_height = 32
        self.rect = pygame.Rect(pos[0], pos[1], self.image_width, self.image_height)
        self.attack_rect = []

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.v = 4

        self.right_k = right_k
        self.left_k = left_k
        self.jump_k = jump_k
        self.attack_k = attack_k
        self.weapon_k = weapon_k
        self.dash_k = dash_k

        self.action = 'idle'#플레이어의 현재 액션 이름
        self.frame = 0 #플레이어의 현재 액션 프레임 상태
        self.flip = False
        self.attack_frame = 0
        self.attack = False
        self.dash = False
        self.dash_tick = 0
        self.weapon = 0
        self.weapon_list = ["normal","long","short","ice_sword","chakram"]
        self.damage = [5,3,12,1,2]
        self.weapon_delay = [15,30,10,30,30]
        self.jam = 0
        self.attack_tick = 0

        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.movement = [0,0]
        self.collisions = {}

        self.hp = 0
        self.heart = 3

        self.y_momentum = 0
        self.air_timer = 0

        self.knockback = False
        self.hit_tick = 0
        self.invin = 0

        self.img_id = ""
        self.attack_img_id = ""
        
        self.animation_database = {} #액션 이름(run, idle...) 에 따른 프레임당 이미지 파일 이름 저장(이미지 파일 저장 X)

        self.particles = []
        self.to_remove = []

        self.color = color

        self.dun_weapons = {"ice_sword":[pygame.image.load("sword\dun_ice_sword.png").convert_alpha(),22],"chakram":[pygame.transform.scale(pygame.image.load("sword\sword_4.png").convert_alpha(),(48,48)),15]}
        self.dun = []



    def physics(self):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        global  screen_shake    
        self.movement = [0, 0]

        if self.moving_right:
            self.movement[0] += self.v
        if self.moving_left:
            self.movement[0] -= self.v
        if self.moving_down:
            self.movement[1] += self.v

        self.movement[1] += self.y_momentum #중력 작용
        self.y_momentum += 0.5

        if self.y_momentum > 12: #중력의 한계 설정
            self.y_momentum = 12

        if self.rect.y > 1600: #플레이어가 떨어졌을 때 다시 위로 올리는 코드
            screen_shake = 30
            self.rect.x, self.rect.y = 964, 600
            for i in range(3):
                self.particles.append([[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()/2], [random.randint(0,20)/5 - 2, random.randint(0,20)/5 - 2], random.randint(12, 16),(255,255,255)])
                self.particles.append([[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()/2], [random.randint(0,20)/5 - 2, random.randint(0,20)/5 - 2], random.randint(12, 16),(30,111,255)])
                self.particles.append([[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()/2], [random.randint(0,20)/5 - 2, random.randint(0,20)/5 - 2], random.randint(12, 16),(0,255,255)])
            self.hp = 0
            if self.heart > 0:
                self.heart -= 1
        
        if self.dash:
            self.dash_tick += 1
            if self.dash_tick < 10:
                if not self.flip:
                    self.movement[0] += self.v*2
                else:
                    self.movement[0] -= self.v*2
                
            elif self.dash_tick > 70:
                self.dash = False
                self.dash_tick = 0


    def key_input(self, event):

        if event.type == KEYDOWN:
            if event.key == self.right_k:
                self.moving_right = True
            elif event.key == self.left_k:
                self.moving_left = True
            # if event.key == K_s:
            #     self.moving_down = True
            elif event.key == self.jump_k:
                if self.air_timer < 6: #공중에 떠있는 시간이 6보다 작으면
                    self.y_momentum = -10 #점프
            elif event.key == self.attack_k:
                if  self.attack_tick == 0:
                    self.attack = True

            elif event.key == self.dash_k:
                self.dash = True

        elif event.type == KEYUP:
            if event.key == self.right_k:
                self.moving_right = False
            elif event.key == self.left_k:
                self.moving_left = False
            # if event.key == K_s:
            #     self.moving_down = False
            elif event.key == self.weapon_k:
                if self.weapon < len(self.weapon_list) - 1:
                    self.weapon += 1
                else:
                    self.weapon = 0


    
    def get_up(self, tiles, map):
        hit_tiles = self.collision_test_get(tiles)
        
        for tile in hit_tiles:
            self.jam += 1
            for i, line in enumerate(tiles):
                if tile in line:
                    j = line.index(tile)
                    map[i] = map[i][:j] + '0' + map[i][j+1:]
                    self.damage[self.weapon] += 1
                    for i in range(5):
                        self.particles.append([[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()/2], [random.randint(0,20)/10 - 1, random.randint(0,20)/10 - 1], random.randint(8, 10),(255,255,255)])
                        self.particles.append([[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()/2], [random.randint(0,20)/10 - 1, random.randint(0,20)/10 - 1], random.randint(8, 10),(0,255,255)])
                    return map  
        return map
    
    def collision_test_get(self, tiles):
        hit_list = []  
        for tile_list in tiles:
            for tile in tile_list:
                if type(tile) == pygame.Rect: #타일이 직사각형일 경우
                    if self.rect.colliderect(tile):#플레이어의 히트박스랑 타일의 충돌 확인
                        hit_list.append(tile)
        return hit_list
    
    def particle_effect(self, scroll, display, tiles):
        if self.action != "idle":
            self.particles.extend([[[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()*0.9], [random.randint(0,20)/10 - 1, 2], random.randint(4, 6), (255,255,255)] for _ in range(5)])

        # 직사각형 타일만 추출하여 새로운 리스트 생성
        tile_rects = [tile for tile_list in tiles for tile in tile_list if isinstance(tile, pygame.Rect)]

        # y 좌표를 기준으로 정렬
        tile_rects.sort(key=lambda rect: rect.y)

        i = 0
        while i < len(self.particles):
            particle = self.particles[i]
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 1

            j = 0
            while j < len(tile_rects):
                tile = tile_rects[j]
                if pygame.Rect(tile).colliderect(pygame.Rect(particle[0][0], particle[0][1], int(particle[2]), int(particle[2]))):
                    particle[1][1] = -particle[1][1] * 0.8
                    particle[1][0] *= 0.8
                    particle[0][1] = tile.top - 1
                    break
                j += 1

            pygame.draw.circle(display, particle[3], [int(particle[0][0]) - scroll[0], int(particle[0][1]) - scroll[1]], int(particle[2]))

            if particle[2] <= 0:
                self.to_remove.append(i)
            i += 1

        # 삭제할 항목을 새로운 리스트에 추가하고, 이후에 한 번에 삭제
        for index in reversed(self.to_remove):
            del self.particles[index]
        self.to_remove.clear()

        if self.dash and self.dash_tick < 10:
            self.particles.extend([[[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()/2], [random.randint(0,20)/10 - 1, 0], random.randint(4, 6),(190,187,198)] for _ in range(5)])
            self.particles.extend([[[self.rect.x + self.image.get_width()/2, self.rect.y + self.image.get_height()/2 + 3], [random.randint(0,20)/10 - 1, 0], random.randint(2, 4),(255,255,255)] for _ in range(5)])

    def animation(self):
        if self.dash and self.dash_tick < 10:
            self.action = 'dash'
            if self.movement[0] >= 0:
                self.flip = False
            else:
                self.flip = True
        else:
            if self.air_timer > 2:
                if self.movement[1] < 0:
                    self.action = 'jump'
                else:
                    self.action = 'down'
                if self.movement[0] >= 0:
                    self.flip = False
                else:
                    self.flip = True
            else:
                if self.movement[0] > 0:
                    self.action = 'run'
                    self.flip = False
                if self.movement[0] < 0:
                    self.action = 'run'
                    self.flip = True
                if self.movement[0] == 0:
                    self.action = 'idle'

        # 애니메이션 업데이트
        self.frame += 1
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0
        self.img_id = self.animation_database[self.action][self.frame]




