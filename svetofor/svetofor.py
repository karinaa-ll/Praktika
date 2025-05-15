import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симулятор перекрёстка")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

traffic_light_ns = "green"
traffic_light_ew = "red"
last_switch_time = pygame.time.get_ticks()
AUTO_MODE = False
SWITCH_INTERVAL = 5000  


cars = []
car_speed = 2
passed_cars = 0

font = pygame.font.SysFont("arial", 20)

def draw_intersection(surface):
    surface.fill((180, 180, 180)) 

    road_color = (50, 50, 50)
    pygame.draw.rect(surface, road_color, (300, 0, 200, HEIGHT)) 
    pygame.draw.rect(surface, road_color, (0, 250, WIDTH, 100))  

    # Разметка (прерывистые линии)
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(surface, WHITE, (398, y, 4, 20))  

    for x in range(0, WIDTH, 40):
        pygame.draw.rect(surface, WHITE, (x, 298, 20, 4)) 

    stop_line_color = (255, 0, 0)

    pygame.draw.line(surface, stop_line_color, (300, 240), (500, 240), 3)

    pygame.draw.line(surface, stop_line_color, (300, 360), (500, 360), 3)

    pygame.draw.line(surface, stop_line_color, (240, 250), (240, 350), 3)

    pygame.draw.line(surface, stop_line_color, (560, 250), (560, 350), 3)

    pygame.draw.rect(surface, (70, 70, 70), (375, 275, 50, 50), border_radius=8)
 

def draw_traffic_lights(surface, light_ns, light_ew):
    pygame.draw.rect(surface, BLACK, (370, 130, 20, 50))  
    pygame.draw.rect(surface, BLACK, (630, 270, 50, 20))  

    pygame.draw.circle(surface, RED if light_ns == "red" else (100, 0, 0), (380, 140), 8)
    pygame.draw.circle(surface, GREEN if light_ns == "green" else (0, 100, 0), (380, 160), 8)

    pygame.draw.circle(surface, RED if light_ew == "red" else (100, 0, 0), (640, 280), 8)
    pygame.draw.circle(surface, GREEN if light_ew == "green" else (0, 100, 0), (660, 280), 8)

def spawn_car():
    direction = random.choice(["north", "south", "east", "west"])
    if direction == "north":
        return [400, HEIGHT, 0, -car_speed, False]
    elif direction == "south":
        return [400, -40, 0, car_speed, False]
    elif direction == "east":
        return [-40, 300, car_speed, 0, False]
    elif direction == "west":
        return [WIDTH, 300, -car_speed, 0, False]

def update_cars(cars, light_ns, light_ew):
    global passed_cars
    for i, car in enumerate(cars[:]):
        x, y, dx, dy, entered = car

        # Координаты зоны перекрёстка
        in_intersection = 250 <= y <= 350 if dx == 0 else 250 <= x <= 550

        blocked = False
        for j, other in enumerate(cars):
            if i == j:
                continue
            ox, oy, odx, ody, _ = other

            if dx == 0 and abs(x - ox) < 40 and 0 < (oy - y) * dy < 50 and abs(ox - x) < 10:
                blocked = True
                break
            if dy == 0 and abs(y - oy) < 40 and 0 < (ox - x) * dx < 50 and abs(oy - y) < 10:
                blocked = True
                break

        if blocked:
            continue  
        
        if not entered:
            if dx == 0: 
                if dy < 0:  
                    stop_y = 360 
                    if y <= stop_y and light_ns == "red":
                        continue
                else:  
                    stop_y = 240 
                    if y + 30 >= stop_y and light_ns == "red":
                        continue

            else:  
                if dx < 0:  
                    stop_x = 560  
                    if x <= stop_x and light_ew == "red":
                        continue
                else:  
                    stop_x = 240  
                    if x + 30 >= stop_x and light_ew == "red":
                        continue

        if not entered and (
            (dx == 0 and light_ns == "green" and in_intersection) or
            (dx != 0 and light_ew == "green" and in_intersection)
        ):
            car[4] = True

        car[0] += dx
        car[1] += dy

        if not (0 <= car[0] <= WIDTH and 0 <= car[1] <= HEIGHT):
            cars.remove(car)
            passed_cars += 1



def draw_cars(surface, cars):
    for x, y, dx, dy, _ in cars:
        color = random.choice([(0, 128, 255), (255, 0, 0), (0, 200, 0), (255, 165, 0)])
        width, height = (30, 15) if dx != 0 else (15, 30)
        pygame.draw.rect(surface, color, (x, y, width, height))


def toggle_lights():
    global traffic_light_ns, traffic_light_ew
    if traffic_light_ns == "green":
        traffic_light_ns = "red"
        traffic_light_ew = "green"
    else:
        traffic_light_ns = "green"
        traffic_light_ew = "red"

def auto_switch():
    global last_switch_time
    now = pygame.time.get_ticks()
    if now - last_switch_time >= SWITCH_INTERVAL:
        toggle_lights()
        last_switch_time = now

def draw_ui():
    pygame.draw.rect(WIN, (220, 220, 220), (0, 0, WIDTH, 40))  # верхняя панель

    manual_btn = font.render("Пробел: переключить", True, BLACK)
    auto_btn = font.render("A: авто режим", True, BLACK)
    counter = font.render(f"Проехало: {passed_cars}", True, BLACK)
    mode = font.render(f"Режим: {'Авто' if AUTO_MODE else 'Ручной'}", True, BLACK)

    WIN.blit(manual_btn, (10, 10))
    WIN.blit(auto_btn, (200, 10))
    WIN.blit(counter, (400, 10))
    WIN.blit(mode, (600, 10))

# Основной цикл
run = True
spawn_timer = 0

while run:
    clock.tick(60)
    spawn_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_lights()
            elif event.key == pygame.K_a:
                AUTO_MODE = not AUTO_MODE

    if AUTO_MODE:
        auto_switch()

    if spawn_timer >= 60:  # Каждую секунду
        cars.append(spawn_car())
        spawn_timer = 0

    update_cars(cars, traffic_light_ns, traffic_light_ew)

    draw_intersection(WIN)
    draw_traffic_lights(WIN, traffic_light_ns, traffic_light_ew)
    draw_cars(WIN, cars)
    draw_ui()

    pygame.display.update()

pygame.quit()
