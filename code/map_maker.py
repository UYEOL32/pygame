import pygame, sys, math,os

from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Pygame Window')

WINDOW_SIZE = (1200,800)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
history = []
display = pygame.Surface(WINDOW_SIZE)


def load_map(path):
    with open((path) + ".txt", "r") as fp:
        return fp.read().splitlines()# = .split('\n')
game_map_ad = 'assets/map4/map'    
jam_map_ad = 'assets/map4/jam_map'
game_map = load_map(game_map_ad)
jam_map = load_map(jam_map_ad)

player_image = pygame.image.load(('player_animations\idle\idle_0.png'))
player_image.set_colorkey((255, 255, 255))#플레이어의 배경색(특정한 색)을 투명색으로 바꾸는 명령

grass_image = pygame.image.load(('assets/grass.png'))
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load(('assets/dirt.png'))

jam_image = pygame.image.load('assets/ability_jam.png')
jam_image = pygame.transform.scale(jam_image,(12,16))
jam_image.set_colorkey((88,88,88))

player_rect = pygame.Rect(250, 50, player_image.get_width(), player_image.get_height())

def draw_grid(surface, width, height, tile_size):
    for x in range(0, width, tile_size):
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, height))
    for y in range(0, height, tile_size):
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))

def collision_test(rect, tiles): 
    for row in tiles:
        for tile in row:
            if rect.colliderect(tile):#플레이어의 히트박스랑 타일의 충돌 확인
                return tile
    
    return -1

def selecting(mouse_rect, tiles):

    tile = collision_test(mouse_rect, tiles)

    if tile != -1:
        print("selected")
        for i, line in enumerate(tiles):
            if tile in line:
                j = line.index(tile)
                return i, j
    return -1, -1

def changing(number,i,j,game_map,path):
    game_map[i] = game_map[i][:j] + str(number) + game_map[i][j+1:]
    print(i,j)
    with open(path + ".txt", "w") as file:
        file.truncate(0)
        for line in game_map:
            for n in line:
                file.write(n)
            file.write("\n")

def double_on(first_i,first_j,second_i,second_j,number,game_map):
    if first_i <= second_i:
        if first_j <= second_j:
            double_changing(first_i,first_j,second_i,second_j,number, game_map)
        else:
            double_changing(first_i,second_j,second_i,first_j,number, game_map)
    else:
        if first_j <= second_j:
            double_changing(second_i,first_j,first_i,second_j,number, game_map)
        else:
            double_changing(second_i,second_j,first_i,first_j,number, game_map)


def double_changing(first_i,first_j,second_i,second_j,number, game_map):
    for i in range(first_i,second_i+1):
        game_map[i] = game_map[i][:first_j] + str(number)*(second_j - first_j + 1) + game_map[i][second_j+1:]

    with open((game_map_ad) + ".txt", "w") as file:
        file.truncate(0)
        for line in game_map:
            for n in line:
                file.write(n)
            file.write("\n")

def J_double_on(first_i,first_j,second_i,second_j,number,game_map):
    if first_i <= second_i:
        if first_j <= second_j:
            J_double_changing(first_i,first_j,second_i,second_j,number, game_map)
        else:
            J_double_changing(first_i,second_j,second_i,first_j,number, game_map)
    else:
        if first_j <= second_j:
            J_double_changing(second_i,first_j,first_i,second_j,number, game_map)
        else:
            J_double_changing(second_i,second_j,first_i,first_j,number, game_map)

def J_double_changing(first_i,first_j,second_i,second_j,number, game_map):
    for i in range(first_i,second_i+1):
        game_map[i] = game_map[i][:first_j] + str(number)*(second_j - first_j + 1) + game_map[i][second_j+1:]

    with open((jam_map_ad) + ".txt", "w") as file:
        file.truncate(0)
        for line in game_map:
            for n in line:
                file.write(n)
            file.write("\n")

def map_clear(game_map,WINDOW_SIZE,TILE_SIZE):
    with open((game_map_ad) + ".txt", "w") as file:
        file.truncate(0)
        for i in range(int(WINDOW_SIZE[1]/TILE_SIZE)):
            for j in range(int(WINDOW_SIZE[0]/TILE_SIZE)):
                file.write("0")
            file.write("\n")

replace_number = 0
double_selecting = False

first_i = -1
second_i = -1
first_j = -1
second_j = -1
i = -1
j = -1

tile_size = 16
width, height = screen.get_size()
grid_surface = pygame.Surface((width, height))
draw_grid(display, width, height, tile_size)

while True:
    display.fill((146,244,255)) #하늘색 배경
    draw_grid(display, width, height, tile_size)
    game_map = load_map(game_map_ad)
    jam_map = load_map(jam_map_ad)

    y = 0
    tile_rects = []

    for row in game_map:
        x = 0
        line = []
        for tile in row:
            
            if tile == "1":
                display.blit(dirt_image,(x*TILE_SIZE,y*TILE_SIZE))
            if tile == "2":
                display.blit(grass_image,(x*TILE_SIZE,y*TILE_SIZE))

            line.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
            x += 1
        tile_rects.append(line)
        y += 1
        
    y = 0
    jam_rects = []

    for row in jam_map:
        x = 0
        line = []
        for tile in row:
            
            if tile == "1":
                display.blit(jam_image,(x*TILE_SIZE,y*TILE_SIZE))

            line.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
            x += 1
        jam_rects.append(line)
        y += 1
    


    

    player_rect.x, player_rect.y = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_3:
                if double_selecting:
                    if first_i and second_i != -1:
                        replace_number = 0
                        double_on(first_i,first_j,second_i,second_j,replace_number,game_map)
                        J_double_on(first_i,first_j,second_i,second_j,replace_number,jam_map)
                else:
                    if i != -1:
                        replace_number = 0
                        changing(replace_number,i,j,game_map,game_map_ad)
                        changing(replace_number,i,j,jam_map,jam_map_ad)

            if event.key == K_4:
                if double_selecting:
                    if first_i and second_i != -1:
                        replace_number = 1
                        J_double_on(first_i,first_j,second_i,second_j,replace_number,jam_map)
                else:       
                    if i != -1:
                        replace_number = 1
                        changing(replace_number,i,j,jam_map,jam_map_ad)

            if event.key == K_1:
                if double_selecting:
                    if first_i and second_i != -1:
                        replace_number = 1
                        double_on(first_i,first_j,second_i,second_j,replace_number,game_map)
                        
                else:
                    if i != -1:
                        replace_number = 1
                        changing(replace_number,i,j,game_map,game_map_ad)

            if event.key == K_2:
                if double_selecting:
                    if first_i and second_i != -1:
                        replace_number = 2
                        double_on(first_i,first_j,second_i,second_j,replace_number,game_map)
                        
                else:
                    if i != -1:
                        replace_number = 2
                        changing(replace_number,i,j,game_map,game_map_ad)

            if event.key == K_LSHIFT:               
                if double_selecting:
                    double_selecting = False
                    print("double_off")
                else:
                    double_selecting = True
                    print("double_on")

            if event.key == K_n:
                history.append(game_map)
                map_clear(game_map,WINDOW_SIZE,TILE_SIZE)
                print("map_clear")

            if event.key == K_BACKSPACE:
                if len(history) != 0:                    
                    with open((game_map_ad) + ".txt", "w") as file:
                        file.truncate(0)
                        for line in history[-1]:
                            for n in line:
                                file.write(n)
                            file.write("\n")   

                    history.pop() # history 리스트에서 가장 최근에 추가된 값을 제거
                    
        if event.type == MOUSEBUTTONDOWN:
            history.append(game_map)
            if double_selecting == False:
                i,j = selecting(player_rect, tile_rects)
            else:
                first_i,first_j = selecting(player_rect, tile_rects)

        if event.type == MOUSEBUTTONUP:
            if double_selecting == True:                
                second_i,second_j = selecting(player_rect, tile_rects)


    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    
    pygame.display.update()
    clock.tick(60)
        




