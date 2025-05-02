import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 650, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Камень, Ножницы, Бумага!')

font = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

rock_image = pygame.image.load('rock.png')  
scissors_image = pygame.image.load('scissors.png') 
paper_image = pygame.image.load('paper.png')  

rock_image = pygame.transform.scale(rock_image, (100, 100))
scissors_image = pygame.transform.scale(scissors_image, (100, 100))
paper_image = pygame.transform.scale(paper_image, (100, 100))

choices = ['Камень', 'Ножницы', 'Бумага']

def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_button(x, y, width, height, color, image):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))
    screen.blit(image, (x + (width - image.get_width()) // 2, y + (height - image.get_height()) // 2))

def draw_image(image, x, y):
    screen.blit(image, (x, y))


def game():

    user_choice = None
    computer_choice = None
    result = ''
    score = {'wins': 0, 'losses': 0, 'ties': 0}

    running = True
    while running:
        screen.fill(WHITE)
        draw_text('Камень Ножницы Бумага!', font, BLACK, 80, 20)

        draw_button(50, 150, 150, 150, GRAY, rock_image)
        draw_button(225, 150, 150, 150, GRAY, scissors_image)
        draw_button(400, 150, 150, 150, GRAY, paper_image)

        if user_choice == 'Камень':
            draw_image(rock_image, 50, 250)
        elif user_choice == 'Ножницы':
            draw_image(scissors_image, 50, 250)
        elif user_choice == 'Бумага':
            draw_image(paper_image, 50, 250)
        
        if computer_choice == 'Камень':
            draw_image(rock_image, 400, 250)
        elif computer_choice == 'Ножницы':
            draw_image(scissors_image, 400, 250)
        elif computer_choice == 'Бумага':
            draw_image(paper_image, 400, 250)

        draw_text('Выберите свой ход (R, P, S) или нажмите кнопку', font_small, BLACK, 50, 100)

        if user_choice is not None:
            draw_text(f'Вы выбрали: {user_choice}', font_small, BLACK, 80, 280)
            draw_text(f'Компьютер выбрал: {computer_choice}', font_small, BLACK, 80, 320)
            draw_text(result, font, GREEN if 'выиграли' in result else RED, 80, 360)

        draw_text(f'Победы: {score["wins"]} Поражения: {score["losses"]} Ничьи: {score["ties"]}', font_small, BLACK, 80, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    user_choice = 'Камень'
                elif event.key == pygame.K_s:  
                    user_choice = 'Ножницы'
                elif event.key == pygame.K_p: 
                    user_choice = 'Бумага'
                elif event.key == pygame.K_SPACE: 
                    user_choice = None
                    computer_choice = None
                    result = ''
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 50 <= mouse_x <= 200 and 150 <= mouse_y <= 300:
                    user_choice = 'Камень'
                elif 225 <= mouse_x <= 375 and 150 <= mouse_y <= 300:
                    user_choice = 'Ножницы'
                elif 400 <= mouse_x <= 550 and 150 <= mouse_y <= 300:
                    user_choice = 'Бумага'

            if user_choice is not None and computer_choice is None:
                computer_choice = random.choice(choices)
                if user_choice == computer_choice:
                    result = 'Ничья!'
                    score['ties'] += 1
                elif (user_choice == 'Камень' and computer_choice == 'Ножницы') or \
                     (user_choice == 'Ножницы' and computer_choice == 'Бумага') or \
                     (user_choice == 'Бумага' and computer_choice == 'Камень'):
                    result = 'Вы выиграли!'
                    score['wins'] += 1
                else:
                    result = 'Вы проиграли!'
                    score['losses'] += 1

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


game()
