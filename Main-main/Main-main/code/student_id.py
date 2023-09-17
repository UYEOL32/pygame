import pygame
import pygame.locals
pygame.init()

def Student_Id(screen,w,h,player_name):


    font = pygame.font.Font("font/NEXONLv1GothicBold.ttf", 36)

    # 텍스트 입력 상자 생성
    input_box = pygame.Rect(w/2 - 100, h/2 - 25, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    input_text = ''

    enabled = True

    clock = pygame.time.Clock()

    def is_numeric(input_str):
        return input_str.isdigit()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(text) == 5 and is_numeric(text):
                            input_text = text
                            text = ''
                            running = False
                        else:
                            enabled = False
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(font.render(player_name +"의 학번 입력", True, color), (w/2-115, h/2 - h/4))

        if not enabled:
            screen.blit(font.render("5자리의 숫자(학번)를 입력해주세요.", True, color), (w/2-275, h/2 + h/4))

        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
    return input_text

