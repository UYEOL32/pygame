import pygame,math

pygame.init()

WINDOW_SIZE = (1920, 1080)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)

game_font = pygame.font.Font("font/NEXONLv1GothicBold.ttf", 40)

# weapon_icon = [pygame.image.load("assets/weapon_icon_0.png"),pygame.image.load("assets/weapon_icon_1.png"),pygame.image.load("assets/weapon_icon_2.png")]

ui = []
for i in range(0,3):
    image = pygame.image.load("assets/UI_"+str(i)+".png").convert_alpha()
    image = pygame.transform.scale(image,(image.get_width()*2,image.get_height()*2))
    image.set_colorkey((255,255,255))
    ui.append(image)


ui_pos = [20,1080 - ui[2].get_height()]

weapon_image = []

for i in range(0,5):
    S_image = pygame.image.load("sword/sword_"+ str(i) + ".png").convert_alpha()
    # S_image.set_colorkey((255,255,255))
    S_image = pygame.transform.scale(S_image,(32*4,32*4))
    weapon_image.append(S_image)
  
def box_maker(w,h,i,color):
    box = pygame.Surface((w,h))
    box.set_alpha(i)
    box.fill(color)
    
    return box

box1 = box_maker(400,80,100,(0,0,0))

def easeOutQuint(t):
    t -= 1
    return t * t * t + 1
    
def UI(display,WINDOW_SIZE,screen,player1,player2,R_WINDOW_SIZE , scroll):

    over_1 = 0
    over_2 = 0

    surf = pygame.transform.scale(display, WINDOW_SIZE)#화면 전체를 표시 WINDOW_SIZE를 바꾸어서 전체 사이즈를 조절 가능
    
    screen.blit(surf, (0, 0))#화면 전체를 표시-> 플레이어 , 타일

    
    player1_red = easeOutQuint(player1.hp/100)*255
    player1_red = math.floor(player1_red)

    if player1_red >= 155:
        over_1 = 10
        if player1_red >= 200:
            over_1 = 20
            if player1_red >= 255:
                over_1 = 30 + player1_red - 255
                if over_1 >= 100:
                    over_1 = 100
                player1_red = 255


    player2_red = easeOutQuint(player2.hp/100)*255
    player2_red = math.floor(player2_red)

    if player2_red >= 155:
        over_2 = 10
        if player2_red >= 200:
            over_2 = 20
            if player2_red >= 255:
                over_2 = 30 + player2_red - 255
                if over_2 >= 100:
                    over_2 = 100
                player2_red = 255

    pygame.draw.circle(screen, [player1_red,100 - over_1,250 - over_1 * 2.5], [142, 957], 115, width=0)
    pygame.draw.circle(screen, [player2_red,100 - over_2,250 - over_2 * 2.5], [1920-142,957], 115, width=0)

    pygame.draw.circle(screen, [255,255,255], [140, 956], 89, width=0)
    pygame.draw.circle(screen, [255,255,255], [1920-140,956], 89, width=0)

    screen.blit(weapon_image[player1.weapon],(75,895))
    screen.blit(pygame.transform.flip(weapon_image[player2.weapon],True,False),(1920-75 - 32*4,895))

    # screen.blit(box1,(WINDOW_SIZE[0]/4*3, WINDOW_SIZE[1]/6*5))
    # screen.blit(box1,(WINDOW_SIZE[0]/4 - box1.get_width(), WINDOW_SIZE[1]/6*5))
   
    # text = game_font.render("jam: " + str(player1.jam) +"   " + player1.weapon_list[player1.weapon],True,(255,255,255))
    # screen.blit(text,(WINDOW_SIZE[0]/4*3 + (box1.get_width()-text.get_width())/2, WINDOW_SIZE[1]/6*5+ (box1.get_height()-text.get_height())/2))

    # text = game_font.render("jam: " + str(player2.jam) +"   "+ player2.weapon_list[player2.weapon],False,(255,255,255))
    # screen.blit(text,(WINDOW_SIZE[0]/4 + (box1.get_width()-text.get_width())/2 - box1.get_width(), WINDOW_SIZE[1]/6*5 + (box1.get_height()-text.get_height())/2))

    screen.blit(game_font.render(str(player2.hp)+ "%",True,(0,0,0)), (WINDOW_SIZE[0]/2- WINDOW_SIZE[0]/10,100))
    screen.blit(game_font.render("vs",True,(224,20,20)), (WINDOW_SIZE[0]/2,100))
    screen.blit(game_font.render(str(player1.hp)+ "%",False,(0,0,0)), (WINDOW_SIZE[0]/2 + WINDOW_SIZE[0]/10,100))

    if player1.heart == 3:
        screen.blit(ui[2],(ui_pos[0],ui_pos[1]))
    elif player1.heart == 2:
        screen.blit(ui[1],(ui_pos[0],ui_pos[1]))
    elif player1.heart == 1:
        screen.blit(ui[0],(ui_pos[0],ui_pos[1]))

    if player2.heart == 3:
        screen.blit(pygame.transform.flip(ui[2],True,False),(1920 - ui[2].get_width() - ui_pos[0],ui_pos[1]))
    elif player2.heart == 2:
        screen.blit(pygame.transform.flip(ui[1],True,False),(1920- ui[1].get_width() -ui_pos[0],ui_pos[1]))
    elif player2.heart == 1:
        screen.blit(pygame.transform.flip(ui[0],True,False),(1920- ui[0].get_width() -ui_pos[0],ui_pos[1]))

    return surf
