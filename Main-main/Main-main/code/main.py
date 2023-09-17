import pygame, sys,random,pickle
from pygame.locals import * # import pygame modules

from ui import UI
from player import Player
from network import Network
from student_id import Student_Id

n = Network()
clock = pygame.time.Clock() # set up the clock


pygame.init() # initiate pygame

pygame.display.set_caption('Pygame Window') # set the window name

WINDOW_SIZE = (1920,1080) # set up window size
global R_WINDOW_SIZE
R_WINDOW_SIZE = [1920,1080] # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen


global img_S
global screen_shake
global winner

winner = -1

img_S = 2
screen_shake = 0

game_font = pygame.font.Font("font/NEXONLv1GothicBold.ttf", 40)

# def (relative_path): #상대 경로 지정(빌드용)
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

display = pygame.Surface(R_WINDOW_SIZE)#화면 전체 즉 모든 fill 과정은 여기서 수행 screen.fill X -> display.fill
#---------------애니메이션--------------------
def palette_swap(surf,old_color,new_color):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_color)
    surf.set_colorkey(old_color)
    img_copy.blit(surf,(0,0))
    return img_copy

def outline(img,loc,color,display):
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

#---------------------------------------------
def weapon_change(self):
    if self.weapon_list[self.weapon] == "normal":
        self.animation_database['attack'] = load_animation(("player_animations/attack"),[2,3,3,2],[1.5,1])
        self.attack_type = 0
    if self.weapon_list[self.weapon] == "long":
        self.animation_database['attack'] = load_animation(("player_animations/attack"),[2,3,3,2],[2.7,1])
        self.attack_type = 0
    if self.weapon_list[self.weapon] == "short":
        self.animation_database['attack'] = load_animation(("player_animations/attack"),[2,3,3,2],[0.8,1.5])
        self.attack_type = 0
    if self.weapon_list[self.weapon] == "ice_sword":
        self.attack_image = self.dun_weapons["ice_sword"][0]
        self.attack_type = 1
    if self.weapon_list[self.weapon] == "chakram":
        self.attack_image = self.dun_weapons["chakram"][0]
        self.attack_type = 1

def attack_cal(self, animation_frames,display):
    if self.attack_tick > 0:
        self.attack_tick +=1
        if self.attack_tick > self.weapon_delay[self.weapon]:
            self.attack_tick = 0

    if self.attack:
        if self.attack_type == 0:
            self.attack_rect.clear()
            self.attack_img_id = self.animation_database["attack"][self.attack_frame]
            self.attack_image =animation_frames[self.attack_img_id]
            self.attack_frame += 1

            k = (self.attack_image.get_height() - self.image.get_height())/2

            if self.flip:
                display.blit(pygame.transform.flip(self.attack_image,True,False), (self.rect.x - self.attack_image.get_width() - scroll[0], self.rect.y - k - scroll[1]))
                self.attack_rect.append(pygame.Rect(self.rect.x - self.attack_image.get_width(), self.rect.y - k, self.attack_image.get_width(), self.attack_image.get_height()))
            else:
                display.blit(self.attack_image,(self.rect.x  + self.image.get_width() - scroll[0], self.rect.y - k - scroll[1]))
                self.attack_rect.append(pygame.Rect(self.rect.x + self.image.get_width() , self.rect.y - k, self.attack_image.get_width(), self.attack_image.get_height()))

            if self.attack_frame >= len(self.animation_database['attack']):
                self.attack_frame = 0
                self.attack_rect.clear()
                self.attack = False
                self.attack_tick = 1

        if self.attack_type == 1:
            
            self.attack = False
            self.attack_tick = 1

            self.dun.append([self.attack_image, self.dun_weapons[self.weapon_list[self.weapon]][1], self.damage[self.weapon], [self.rect.x,self.rect.y], 0, self.flip]) #이미지, 속도, 데미지 , 현재 위치, 수명 ,플립

def dun_attack_cal(self,display,tiles,another):
    for i in self.dun:
        self.attack_rect.clear()
        if i[0] == self.dun_weapons["ice_sword"][0]:
            if i[5]:
                i[3][0] -= i[1]
                display.blit(pygame.transform.flip(i[0],True,False), (i[3][0] - self.attack_image.get_width() - scroll[0], i[3][1] - scroll[1]))
                self.attack_rect.append(pygame.Rect(i[3][0] - self.attack_image.get_width(), i[3][1], i[0].get_width(), i[0].get_height()))
                i[4] += 1

                if i[4] > 25:
                    self.dun.remove(i)
            else:
                i[3][0] += i[1]
                display.blit(i[0], (i[3][0] + self.image.get_width() - scroll[0], i[3][1] - scroll[1]))
                self.attack_rect.append(pygame.Rect(i[3][0] + self.image.get_width(), i[3][1], i[0].get_width(), i[0].get_height()))
                i[4] += 1

                if i[4] > 25:
                    self.dun.remove(i)
        else:
            if self.flip:
                i[3][0] -= i[1]
                display.blit(pygame.transform.flip(i[0],True,i[4] %2 == 1), (i[3][0] - self.attack_image.get_width() - scroll[0], i[3][1] - scroll[1] - 10))
                self.attack_rect.append(pygame.Rect(i[3][0] - self.attack_image.get_width(), i[3][1] - 10, i[0].get_width(), i[0].get_height()))
                i[4] += 1

                if i[4] > 25:
                    self.dun.remove(i)
            else:
                i[3][0] += i[1]
                display.blit(pygame.transform.flip(i[0],False,i[4] %2 == 1), (i[3][0] + self.image.get_width() - scroll[0], i[3][1] - scroll[1] - 10))
                self.attack_rect.append(pygame.Rect(i[3][0] + self.image.get_width(), i[3][1] - 10, i[0].get_width(), i[0].get_height()))
                i[4] += 1

                if i[4] > 25:
                    self.dun.remove(i)

        if i[4] <=25:
            if collision_test(pygame.Rect(i[3][0] + self.image.get_width(), i[3][1] - 10, i[0].get_width(), i[0].get_height()),tiles):
                
                self.dun.remove(i)
            elif pygame.Rect(i[3][0] + self.image.get_width(), i[3][1] - 10, i[0].get_width(), i[0].get_height()).colliderect(another.rect):
                
                self.dun.remove(i)


            

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

def player_setting(self):
    global animation_frames
    self.image = pygame.image.load(('player_animations/idle/idle_0.png')).convert_alpha()
    self.image = pygame.transform.scale(self.image,(self.image.get_width()*img_S/2, self.image.get_height()*img_S/2))
    self.image.set_colorkey((255, 255, 255) )#플레이어의 배경색(특정한 색)을 투명색으로 바꾸는 명령

    self.attack_image = pygame.image.load(('player_animations/idle/idle_0.png')).convert_alpha()


    self.animation_database['run'] = load_animation(("player_animations/run"),[4,4,4,4,4,4],[0.7,0.7]) #사진 하나당 7프레임, 7프레임 / 달리는 상태
    self.animation_database['idle'] = load_animation(("player_animations/idle"),[7,7,7,50],[0.7,0.7]) #사진 하나당 7프레임, 7프레임, 40프레임 / 쉬는 상태
    self.animation_database['attack'] = load_animation(("player_animations/attack"),[2,3,3,2],[1.5,1]) 
    self.animation_database['jump'] = load_animation(("player_animations/jump"),[4,3,3,3],[0.7,0.7]) #사진 하나당 7프레임, 7프레임 / 달리는 상태
    self.animation_database['dash'] = load_animation(("player_animations/dash"),[3,3],[0.7,0.7]) #사진 하나당 7프레임, 7프레임 / 달리는 상태
    self.animation_database['down'] = load_animation(("player_animations/down"),[4,3],[0.7,0.7]) #사진 하나당 7프레임, 7프레임 / 달리는 상태

def character_blit(self,scroll,display):
    self.image = animation_frames[self.img_id] #이름을 이미지 파일로 변환하여 player_image에 저장
    outline(pygame.transform.flip(self.image,self.flip,False),[self.rect.x - scroll[0], self.rect.y - scroll[1]],self.color,display)
    display.blit(pygame.transform.flip(self.image,self.flip,False), (self.rect.x - scroll[0], self.rect.y - scroll[1])) #display에 플레이어 그리기(screen X), pygame.transform.flip(이미지,x축 대칭,y축 대칭)

#-----------------------------------------

def change_action(action_var,frame,new_value):
    if action_var != new_value: #기존 액션 동작이 새 동작과 다른 경우
        action_var = new_value #기존 액션 동작을 새 액션 동작으로 바꿈
        frame = 0 #해당 동작의 이미지 프레임을 0으로 설정(초기화)
    return action_var, frame

#---------------------------------------------

global background_image
background_image = pygame.image.load('assets/background_1.jpg').convert_alpha()
background_image = pygame.transform.scale(background_image,(1920,1080))

grass_image = pygame.image.load(('assets/grass.png')).convert_alpha()

dirt_image = pygame.image.load('assets/dirt.png').convert_alpha()

jam_image = pygame.image.load('assets/ability_jam.png').convert_alpha()
jam_image = pygame.transform.scale(jam_image,(24,27))
jam_image.set_colorkey((88,88,88))

TILE_SIZE = grass_image.get_width()*img_S

grass_image = pygame.transform.scale(grass_image,(TILE_SIZE,TILE_SIZE))
dirt_image = pygame.transform.scale(dirt_image,(TILE_SIZE,TILE_SIZE))


#---------기본 설정----------------------
#맵 파일

def load_map(path):
    with open((path) + ".txt", "r") as fp:
        return fp.read().splitlines()# = .split('\n')
#------------물리 엔진 함수 --------------------
def collision_test(rect, tiles):
    hit_list = []  
    for tile in tiles:
        if rect.colliderect(tile):#플레이어의 히트박스랑 타일의 충돌 확인
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles,dt):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += movement[0]*dt #플레이어의 렉트의 x좌표를 움직임

    hit_list = collision_test(rect, tiles) #함수 호출후 hit_list의 값을 받아 hit_list에 값이 있을 경우 아레 for문 실행
    for tile in hit_list:
        if movement[0] > 0: #오른쪽으로 이동
            rect.right = tile.left #플레이어의 오른쪽과 타일의 왼쪽의 좌표를 같게 함, 즉 정지 상태를 유지하도록 하는 기능
            collision_types['right'] = True #플레이어의 현재 운동 상태를 딕셔너리에 저장
        elif movement[0] < 0:   #왼쪽으로 이동
            rect.left = tile.right #왼쪽 = 오른쪽
            collision_types['left'] = True

    rect.y += movement[1]*dt #플레이어의 렉트의 y좌표를 움직임
    
    hit_list = collision_test(rect, tiles) #이하 동일
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
            

    return rect, collision_types

def easeInCirc(t):
    if t > 80:
        return t*t/800
    return t/10

def knockback(player1,player2): #player2 = 공격자, player1 = 피격자
    global screen_shake
    for i in range(3 + int(easeInCirc(player1.hp)/14)):
        player1.particles.append([[player1.rect.x + player1.image.get_width()/2, player1.rect.y + player1.image.get_height()/2], [random.randint(0,20)/5 - 2, random.randint(0,20)/5 - 2], random.randint(2, 6),(190,187,198)])
        player1.particles.append([[player1.rect.x + player1.image.get_width()/2, player1.rect.y + player1.image.get_height()/2], [random.randint(0,20)/5 - 2, random.randint(0,20)/5 - 2], random.randint(2, 6),(248,70,70)])
    if player2.air_timer > 2:
        player1.movement[1] -= int((easeInCirc(player1.hp)*1.5 + 3)/2)
    
    if player1.rect.x - player2.rect.x > 0:
        player1.movement[0] += int(easeInCirc(player1.hp)*1.5 + 5)
    else:
        player1.movement[0] -= int(easeInCirc(player1.hp)*1.5 + 5)
    
    if int(easeInCirc(player1.hp) + 0.1) > 70:
        screen_shake = 10

    return player1.movement

def damage_manager(player1,player2): #player2 = 공격자, player1 = 피격자
    for rect in player2.attack_rect:
        if player1.invin == 0:
            if player1.rect.colliderect(rect):
                if player2.dash:
                    player1.hp += player2.damage[player2.weapon]
                player1.hp += player2.damage[player2.weapon]
                player1.hp = int(player1.hp)
                player1.knockback = True
                player1.hit_tick = 0


    if player1.knockback:
        if player1.invin == 0:
            player1.movement = knockback(player1, player2)
            player1.invin = 1
        else:
            player1.invin += 1
            if player1.invin <= 8:
                player1.movement = knockback(player1, player2)
            elif player1.invin >= 10:
                player1.invin = 0
                
                player1.knockback = False

def camera_transform(R_WINDOW_SIZE,scroll,players): 
    cv = 1 #camera velocity
    x = 0
    y = 0
    n = len(players)
    for p in players:
        x += p.rect.x
        y += p.rect.y

    scroll[0] += int((x/n - scroll[0] - R_WINDOW_SIZE[0]/2) / cv)
    #플레이어 카메라 고정, 이 값을 나누면 플레이어를 카메라가 느린 속도로 따라감으로 역동성있는 카메라를 구현 가능
    #-> 픽셀은 소수값을 가지지 못하기 때문에 위의 식이 float형태로 나올 경우 블록이 버벅이는 현상이 발생할 수도 있음
    #->scroll -> scroll
    scroll[1] += int((y/n - scroll[1] - R_WINDOW_SIZE[1]/2) / cv + 4)
    
    return scroll

scroll = [0,0] #x,y 으로 얼마나 카메라가 이동했는지
    
#--------------------------
time_acceleration = 15
prev_time = pygame.time.get_ticks()/time_acceleration 

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#-------------------------

def main():
    global img_S
    global screen_shake
    global animation_frames
    global scroll
    global background_image

    ui = False
    ui_image = pygame.image.load("assets/winner_ui.png").convert_alpha()
    p2_mark = pygame.image.load("assets/1p_mark.png").convert_alpha()
    p1_mark = pygame.image.load("assets/2p_mark.png").convert_alpha()

    p1_mark = pygame.transform.scale(p1_mark,(p1_mark.get_width()/4,p1_mark.get_height()/4))
    p2_mark = pygame.transform.scale(p2_mark,(p2_mark.get_width()/4,p2_mark.get_height()/4))
    ui_image.set_colorkey((255,255,255))

    WINDOW_SIZE = (1920,1080) # set up window size

    R_WINDOW_SIZE = [1920,1080] # set up window size
    
    time_acceleration = 15
    prev_time = pygame.time.get_ticks()/time_acceleration 

    animation_frames = {} # 이미지 파일 이름에 따른 이미지(pygame.image.load)형태로 저장
    game_map_list = [["assets/map1/map",(1800,100),(150,100)],["assets/map3/map",(1050,900),(750,1000)]]
    jam_map_list = ["assets/map1/jam_map"]

    map_id = 0

    game_map_path = game_map_list[map_id][0]
    jam_map_path = jam_map_list[0]

    game_map = load_map(game_map_path)
    jam_map = load_map(jam_map_path)
    
    player2 = Player(game_map_list[map_id][2],K_d,K_a,K_w,K_SPACE,K_h,K_g,(255,0,0))
    player1 = Player(game_map_list[map_id][1],K_RIGHT,K_LEFT,K_UP,K_KP0,K_KP3,K_KP2,(0,0,255))

    player_setting(player1)
    player_setting(player2)

    scroll = [0,0] #x,y 으로 얼마나 카메라가 이동했는지

    camera_players = [player1,player2]  
    p1_student_id = Student_Id(screen,WINDOW_SIZE[0],WINDOW_SIZE[1],"1P")
    p2_student_id = Student_Id(screen,WINDOW_SIZE[0],WINDOW_SIZE[1],"2P")

    Running  = True

    while Running: 

        current_time = pygame.time.get_ticks()/time_acceleration 
        elapsed_time = current_time - prev_time
        prev_time = current_time

        #-------카메라 설정---------------------

        
        scroll = camera_transform(R_WINDOW_SIZE,scroll,camera_players)

        

        if screen_shake > 0:#화면 흔들기
            screen_shake -= 1
        
        if screen_shake:
            scroll[0] += random.randint(0,6) -3
            scroll[1] += random.randint(0,6) -3

        # 두 플레이어 간의 거리 계산
        distance_x = abs(player1.rect.centerx - player2.rect.centerx)
        distance_y = abs(player1.rect.centery - player2.rect.centery)

        # 거리에 따라 화면 크기 조정
        if distance_x > int(R_WINDOW_SIZE[0] * 0.6):
            R_WINDOW_SIZE[0] += 8/2
            R_WINDOW_SIZE[1] += 4.5/2
        elif distance_x < int(R_WINDOW_SIZE[0] * 0.5):
            R_WINDOW_SIZE[0] -= 8/2
            R_WINDOW_SIZE[1] -= 4.5/2
        
        if distance_y > int(R_WINDOW_SIZE[1] * 0.8):
            R_WINDOW_SIZE[0] += 8/2
            R_WINDOW_SIZE[1] += 4.5/2

        # 한 플레이어가 화면 밖으로 벗어나면 화면 크기 증가
        if player1.rect.x < scroll[0] or player1.rect.right > scroll[0] + R_WINDOW_SIZE[0]:
            R_WINDOW_SIZE[0] += 8/2
            R_WINDOW_SIZE[1] += 4.5/2
        elif player2.rect.x < scroll[0] or player2.rect.right > scroll[0] + R_WINDOW_SIZE[0]:
            R_WINDOW_SIZE[0] += 8/2
            R_WINDOW_SIZE[1] += 4.5/2

        # R_WINDOW_SIZE가 최소값보다 작아지지 않도록 조건문 추가
        if R_WINDOW_SIZE[0] < 640:
            R_WINDOW_SIZE[0] = 640
            R_WINDOW_SIZE[1] = 360

        # R_WINDOW_SIZE가 최대값보다 커지지 않도록 조건문 추가
        if R_WINDOW_SIZE[0] > 1920:
            R_WINDOW_SIZE[0] = 1920
            R_WINDOW_SIZE[1] = 1080
    #---------------------------------------
        display = pygame.Surface((int(R_WINDOW_SIZE[0]),int(R_WINDOW_SIZE[1])))#화면 비율 변화시 적용

        display.fill((146,244,255)) #하늘색 배경

        game_map = load_map(game_map_path)

    #----------------map---------------------------
        tile_rects = []
        tile_group = pygame.sprite.Group()
        y = 0
        for row in game_map:#game_map  리스트를 바탕으로 반복문을 통해 맵 제작
            x = 0
            for tile in row:
                if tile == '1':#흙 이미지 생성
                    tile_image = dirt_image.subsurface((0, 0, TILE_SIZE, TILE_SIZE))
                    tile_group.add(Tile(tile_image,x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':#잔디 이미지 생성
                    tile_image = grass_image.subsurface((0, 0, TILE_SIZE, TILE_SIZE))
                    tile_group.add(Tile(tile_image,x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile != '0':#타일 충돌 감지용 사각형 생성
                    tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))#tile_rects 리스트에 해당 타일 위치에 리스트 값 추가, 
                    #실제 사각형을 display 하는것은 아님
                x += 1
            y += 1
        tile_group.draw(display)
        y = 0
        jam_rects = []

        jam_group = pygame.sprite.Group()

        for row in jam_map:
            x = 0
            line = []
            for tile in row:
                
                if tile == "1":
                    jam_group.add(Tile(jam_image,x*TILE_SIZE - scroll[0],y*TILE_SIZE - scroll[1]))
                    line.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    line.append(0)
                x += 1
            jam_rects.append(line)
            y += 1
        
        jam_group.draw(display)
        #-------------------플레이어--------------------
        weapon_change(player1)#무기 교환 처리6
        weapon_change(player2)

        player1.physics() #플레이어의 물리적 상태를 업데이트
        player2.physics()

        

        jam_map = player1.get_up(jam_rects,jam_map) 
        jam_map = player2.get_up(jam_rects,jam_map)


        #---------------------------------------
        
        dun_attack_cal(player1,display,tile_rects,player2)
        dun_attack_cal(player2,display,tile_rects,player1)

        attack_cal(player1,animation_frames,display)#플레이어 공격 애니메이션 처리
        attack_cal(player2,animation_frames,display)

        damage_manager(player1,player2)
        damage_manager(player2,player1)
        player1.attack_rect.clear()
        player2.attack_rect.clear()
                
        player1.rect, player1.collisions = move(player1.rect, player1.movement, tile_rects,elapsed_time) #플레이어의 위치를 속도를 통해 변화 한 값을 받아옴
        player2.rect, player2.collisions = move(player2.rect, player2.movement, tile_rects,elapsed_time) #플레이어의 위치를 속도를 통해 변화 한 값을 받아옴

        #--------------------플레이어 충돌 감지-------------
        if player1.collisions['bottom']: #플레이어의 현재 상태가 바닥에 닿아 있으면
            player1.y_momentum = 0 #중력 제거
            player1.air_timer = 0
        else:
            player1.air_timer += 1 #공중에 떠있는 시간 

        if player2.collisions['bottom']: #플레이어의 현재 상태가 바닥에 닿아 있으면
            player2.y_momentum = 0 #중력 제거
            player2.air_timer = 0
        else:
            player2.air_timer += 1 #공중에 떠있는 시간 
            
        player1.animation()
        player2.animation()

        character_blit(player1,scroll,display)
        character_blit(player2,scroll,display)

        player1.particle_effect(scroll,display,tile_rects)
        player2.particle_effect(scroll,display,tile_rects)

        

        



    #----------------------------------------------------
        #키입력 감지
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                pygame.quit() # stop pygame
                sys.exit() # stop script21`4QW  EAEE`
            player1.key_input(event)
            player2.key_input(event)
            if event.type == KEYDOWN:
                if event.key == K_1:
                    camera_players = [player1]
                if event.key == K_2:
                    camera_players = [player2]
                if event.key == K_3:
                    camera_players = [player1,player2]
                if event.key == K_ESCAPE:
                    Running = False
                if event.key == K_F1:
                    if not ui:
                        ui = True
                    else:
                        ui = False

    #-----------------------------------------------
        display.blit(p1_mark,(player1.rect.x   -3 - scroll[0],player1.rect.y - 50 - scroll[1]))
        display.blit(p2_mark,(player2.rect.x  -3 - scroll[0],player2.rect.y - 50 - scroll[1]))
    
        surf = UI(display,WINDOW_SIZE,screen,player2,player1,R_WINDOW_SIZE,scroll) #ui 생성

    
        if ui:
            screen.blit(ui_image,(0,0))
        
        if player1.heart == 0 or player2.heart == 0: #게임 종료 조건
            if player1.heart == 0:
                winner = player2
                winner_name = p2_student_id  
                            
            else:
                winner = player1
                winner_name = p1_student_id 

            n.send(winner_name + ":400" )
            game_font = pygame.font.Font("font\Daydream.ttf", 100)
            box = pygame.image.load("assets/black.png").convert_alpha()
            
            player_image = pygame.transform.scale(winner.image,(winner.image.get_width()*20, winner.image.get_height()*20))

            for y in range(0,55):
                screen.blit(box,(0,-1080 + 10*y))
                screen.blit(box,(0,1080 - 10*y))
                pygame.display.update()
                pygame.time.delay(3)
            
            pygame.time.delay(1000)

            for y in range(0,55):
                screen.fill((146,244,255))
                screen.blit(player_image, (1100, 300))
                outline(player_image,(1100, 300),winner.color,screen)
                screen.blit(box,(0,-540 - 10*y))
                screen.blit(box,(0,540 + 10*y))
                pygame.display.update()
                pygame.time.delay(3)

            screen.blit(game_font.render("WINNER",True,(0,0,0)), (100,550))
            pygame.display.update()

            pygame.time.delay(1000)

            screen.blit(game_font.render(winner_name,True,winner.color), (300,850))

            pygame.display.update()

            pygame.time.delay(4000)

            
            Running = False
        
        pygame.display.update() # 디스플레이(변수 display아님) 업데이트

        # fps = str(int(clock.get_fps()))
        # print("현재 프레임: " + fps)

        clock.tick(60) #초당 프레임 수
while True:
    main()

    