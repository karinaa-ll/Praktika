import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поймай Призрака!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("arial", 32)
big_font = pygame.font.SysFont("arial", 48)

GHOST_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(GHOST_SPAWN, random.randint(1000, 2000)) 
GAME_DURATION = 30_000 

ghost_img = pygame.image.load("prizrak.png")
ghost_img = pygame.transform.scale(ghost_img, (100, 100))  

try:
    catch_sound = pygame.mixer.Sound("catch.wav") 
except:
    catch_sound = None

def reset_game():
    return {
        "score": 0,
        "ghost_rect": None,
        "ghost_timer": 0,
        "start_time": pygame.time.get_ticks(),
        "game_over": False
    }

state = reset_game()

clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()
    elapsed = current_time - state["start_time"]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state["game_over"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = reset_game()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and state["ghost_rect"]:
                if state["ghost_rect"].collidepoint(event.pos):
                    state["score"] += 1
                    if catch_sound:
                        catch_sound.play()
                    state["ghost_rect"] = None 

            if event.type == GHOST_SPAWN:
                x = random.randint(0, WIDTH - 100)
                y = random.randint(100, HEIGHT - 100)
                state["ghost_rect"] = pygame.Rect(x, y, 100, 100)
                state["ghost_timer"] = current_time

                pygame.time.set_timer(GHOST_SPAWN, random.randint(1000, 2000))

    if state["ghost_rect"] and current_time - state["ghost_timer"] > 700:
        state["ghost_rect"] = None

    if elapsed >= GAME_DURATION:
        state["game_over"] = True

    screen.fill((240, 240, 240)) 

    title = big_font.render("Поймай Призрака!", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

    tip = font.render("Кликай по призраку, пока не закончится время!", True, BLACK)
    screen.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 60))

    score_text = font.render(f"Счёт: {state['score']}", True, BLACK)
    screen.blit(score_text, (10, 10))

    time_left = max(0, (GAME_DURATION - elapsed) // 1000)
    timer_text = font.render(f"Время: {time_left}", True, BLACK)
    screen.blit(timer_text, (WIDTH - 150, 10))

    if state["ghost_rect"]:
        screen.blit(ghost_img, state["ghost_rect"])

    if state["game_over"]:
        over_text = big_font.render(f"Время вышло! Ваш счёт: {state['score']}", True, BLACK)
        retry_text = font.render("Нажмите ПРОБЕЛ, чтобы начать заново.", True, BLACK)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
