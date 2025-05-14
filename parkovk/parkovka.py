import pygame
import random
import time

pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PARKING_SIZE = 20  # Количество парковочных мест
SLOT_SIZE = 60  # Размер ячеек парковки
PARKING_WIDTH = 5  # Количество колонок на парковке
PARKING_HEIGHT = PARKING_SIZE // PARKING_WIDTH  # Количество строк на парковке
SLOT_COLOR_EMPTY = (34, 139, 34)  # Легкий зеленый (свободно)
SLOT_COLOR_OCCUPIED = (178, 34, 34)  # Темный красный (занято)
BUTTON_COLOR = (70, 130, 180)  # Цвет кнопок
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Автоматизированная парковка")

# Шрифт для текста
font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 20)

parking_slots = [None] * PARKING_SIZE  
entry_queue = []  

# Функция для отрисовки парковки
def draw_parking(surface, slots):
    for i in range(PARKING_SIZE):
        x = (i % PARKING_WIDTH) * SLOT_SIZE + 50  
        y = (i // PARKING_WIDTH) * SLOT_SIZE + 50  
        
        if slots[i] is None:
            color = SLOT_COLOR_EMPTY
        else:
            color = slots[i]["color"]

        pygame.draw.rect(surface, color, (x, y, SLOT_SIZE - 10, SLOT_SIZE - 10), border_radius=8)

# Функция для создания случайной машины
def generate_car():
    car_types = ["легковая", "грузовая", "электромобиль"]
    car_sizes = {"легковая": 1, "грузовая": 2, "электромобиль": 1}
    car_type = random.choice(car_types)
    car_size = car_sizes[car_type]
    car_plate = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))
    car_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return {"plate": car_plate, "type": car_type, "size": car_size, "color": car_color}

# Функция для размещения машины на стоянке
def park_car(car):
    for i in range(PARKING_SIZE):
        if i + car["size"] <= PARKING_SIZE and all(parking_slots[j] is None for j in range(i, i + car["size"])):
            for j in range(i, i + car["size"]):
                parking_slots[j] = car
            return True
    return False


def remove_random_car():
    plates = list({slot["plate"] for slot in parking_slots if slot is not None})
    if not plates:
        return
    target_plate = random.choice(plates)
    for i in range(PARKING_SIZE):
        if parking_slots[i] and parking_slots[i]["plate"] == target_plate:
            parking_slots[i] = None


def draw_ui(surface, entry_queue, occupied, available):
    status_text = font.render(f"Занято: {occupied}  Свободно: {available}", True, WHITE)
    surface.blit(status_text, (10, 10))

    pygame.draw.rect(surface, BUTTON_COLOR, (50, SCREEN_HEIGHT - 120, 200, 50), border_radius=10)
    button_text = button_font.render("Впустить машину", True, WHITE)
    surface.blit(button_text, (60, SCREEN_HEIGHT - 110))

    pygame.draw.rect(surface, BUTTON_COLOR, (300, SCREEN_HEIGHT - 120, 250, 50), border_radius=10)
    button_text = button_font.render("Выпустить случайную машину", True, WHITE)
    surface.blit(button_text, (310, SCREEN_HEIGHT - 110))

    unique_cars = {}
    for slot in parking_slots:
        if slot is not None:
            unique_cars[slot["plate"]] = slot

    title = font.render("На парковке:", True, WHITE)
    surface.blit(title, (SCREEN_WIDTH - 250, 20))

    y_offset = 60
    for car in unique_cars.values():
        car_text = font.render(f"{car['plate']} | {car['size']}", True, car["color"])
        surface.blit(car_text, (SCREEN_WIDTH - 250, y_offset))
        y_offset += 30

    entry_title = font.render("Очередь на въезд:", True, WHITE)
    surface.blit(entry_title, (SCREEN_WIDTH - 250, y_offset + 20))
    y_offset += 60

    for car in entry_queue:
        car_text = font.render(f"{car['plate']} | {car['size']}", True, car["color"])
        surface.blit(car_text, (SCREEN_WIDTH - 250, y_offset))
        y_offset += 30

# Обработка нажатий кнопок
def handle_click(x, y):
    global entry_queue
    if 50 <= x <= 250 and SCREEN_HEIGHT - 120 <= y <= SCREEN_HEIGHT - 70:
        if not entry_queue:
            entry_queue.append(generate_car())
        else:
            car = entry_queue[0]
            if park_car(car):
                entry_queue.pop(0)
            else:
                print("Нет мест")
    elif 300 <= x <= 550 and SCREEN_HEIGHT - 120 <= y <= SCREEN_HEIGHT - 70:
        remove_random_car()

# Главный цикл программы
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(GRAY)
        draw_parking(screen, parking_slots)
        occupied = sum(1 for slot in parking_slots if slot is not None)
        available = PARKING_SIZE - occupied
        draw_ui(screen, entry_queue, occupied, available)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(*event.pos)

        pygame.display.update()
        clock.tick(60)

main()
pygame.quit()