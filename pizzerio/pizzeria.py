import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пиццерия")

FONT = pygame.font.SysFont("arial", 24)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Состояния экрана
MAIN_MENU = "main_menu"
CATEGORY_SELECTION = "category_selection"
ORDER_CREATION = "order_creation"
PIZZA_SIZE_SELECTION = "pizza_size_selection"
PIZZA_DOUGH_SELECTION = "pizza_dough_selection"
PIZZA_TOPPINGS_SELECTION = "pizza_toppings_selection"
PIZZA_CONFIRMATION = "pizza_confirmation"
DRINK_SELECTION = "drink_selection"
DRINK_SIZE_SELECTION = "drink_size_selection"
DRINK_CONFIRMATION = "drink_confirmation"
ORDER_STATUS = "order_status"  # новое состояние

state = MAIN_MENU
current_order = []

selected_pizza_name = ""
selected_size = None
selected_dough = None
selected_toppings = []

selected_drink_name = ""
selected_drink_size = None

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(SCREEN, LIGHT_BLUE, self.rect)
        pygame.draw.rect(SCREEN, BLACK, self.rect, 2)
        text_surf = FONT.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        SCREEN.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Pizza(MenuItem):
    def __init__(self, name, price, size=None, dough=None, toppings=None):
        super().__init__(name, price)
        self.size = size
        self.dough = dough
        self.toppings = toppings or []

    def get_description(self):
        return f"{self.name} ({self.size}, {self.dough}, {', '.join(self.toppings)}) - {self.price}₸"

class Drink(MenuItem):
    def __init__(self, name, price, size=None):
        super().__init__(name, price)
        self.size = size

    def get_description(self):
        return f"{self.name} ({self.size}) - {self.price}₸"

pizza_menu = ["Маргарита", "Пепперони", "Гавайская"]

sizes = {"Маленькая": 0, "Средняя": 500, "Большая": 1000}
dough_types = {"Тонкое": 0, "Толстое": 200}
available_toppings = {"Сыр": 300, "Грибы": 300, "Помидоры": 300, "Оливки": 300, "Пепперони": 300}
drinks_menu = ["Кола", "Спрайт", "Минеральная вода"]
drink_sizes = {"Маленький стакан": 450, "Средний стакан": 800, "Большой стакан": 135}

def main_menu():
    SCREEN.fill(WHITE)
    title = FONT.render("Добро пожаловать в Пиццерию!", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    start_button = Button(WIDTH // 2 - 100, 200, 200, 50, "Начать заказ", action="start_order")
    start_button.draw()
    return [start_button]

def category_selection_screen():
    SCREEN.fill(WHITE)
    title = FONT.render("Выберите категорию:", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    pizza_button = Button(WIDTH // 2 - 100, 150, 200, 50, "Пиццы", action="pizza_category")
    drink_button = Button(WIDTH // 2 - 100, 220, 200, 50, "Напитки", action="drink_category")
    order_button = Button(WIDTH // 2 - 100, 290, 200, 50, "Оформить заказ", action="checkout")  # новая кнопка

    pizza_button.draw()
    drink_button.draw()
    order_button.draw()

    return [pizza_button, drink_button, order_button]

def order_status_screen():
    SCREEN.fill(WHITE)
    title = FONT.render("Статус заказа:", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    y = 80
    total = 0
    for item in current_order:
        SCREEN.blit(FONT.render(item.get_description(), True, BLACK), (50, y))
        y += 30
        total += item.price

    SCREEN.blit(FONT.render(f"Итого к оплате: {total}₸", True, BLACK), (50, y + 10))

    back_button = Button(WIDTH // 2 - 100, y + 60, 200, 50, "Вернуться", action="back_to_category")
    back_button.draw()

    return [back_button]

def order_creation_screen():
    SCREEN.fill(WHITE)
    title = FONT.render("Создание заказа", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    y = 80
    buttons = []
    for pizza in pizza_menu:
        button = Button(WIDTH // 2 - 100, y, 200, 40, pizza, action=pizza)
        button.draw()
        buttons.append(button)
        y += 50
    display_current_order(50, y + 30)
    return buttons

def drink_selection_screen():
    SCREEN.fill(WHITE)
    title = FONT.render("Выберите напиток:", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    y = 120
    buttons = []
    for drink in drinks_menu:
        button = Button(WIDTH // 2 - 100, y, 200, 40, drink, action=drink)
        button.draw()
        buttons.append(button)
        y += 50
    return buttons

def pizza_size_selection(pizza_name):
    SCREEN.fill(WHITE)
    prompt = FONT.render(f"Выберите размер пиццы: {pizza_name}", True, BLACK)
    SCREEN.blit(prompt, (50, 50))
    y = 120
    buttons = []
    for size, price in sizes.items():
        button = Button(100, y, 200, 40, f"{size} (+{price}₸)", action=size)
        button.draw()
        buttons.append(button)
        y += 60
    return buttons

def drink_size_selection(drink_name):
    SCREEN.fill(WHITE)
    prompt = FONT.render(f"Выберите размер стакана: {drink_name}", True, BLACK)
    SCREEN.blit(prompt, (50, 50))
    y = 120
    buttons = []
    for size, price in drink_sizes.items():
        button = Button(100, y, 200, 40, f"{size} (+{price}₸)", action=size)
        button.draw()
        buttons.append(button)
        y += 60
    return buttons

def pizza_dough_selection():
    SCREEN.fill(WHITE)
    prompt = FONT.render(f"Выберите тесто:", True, BLACK)
    SCREEN.blit(prompt, (50, 50))
    y = 120
    buttons = []
    for dough, price in dough_types.items():
        button = Button(100, y, 200, 40, f"{dough} (+{price}₸)", action=dough)
        button.draw()
        buttons.append(button)
        y += 60
    return buttons

def pizza_toppings_selection():
    SCREEN.fill(WHITE)
    prompt = FONT.render(f"Выберите добавки (кликните):", True, BLACK)
    SCREEN.blit(prompt, (50, 50))
    y = 120
    buttons = []
    for topping, price in available_toppings.items():
        text = f"{topping} (+{price}₸)"
        if topping in selected_toppings:
            text = "✓ " + text
        button = Button(100, y, 300, 40, text, action=topping)
        button.draw()
        buttons.append(button)
        y += 50
    confirm_button = Button(WIDTH // 2 - 100, 450, 200, 40, "Подтвердить пиццу", action="confirm_pizza")
    confirm_button.draw()
    buttons.append(confirm_button)
    return buttons

def pizza_confirmation():
    SCREEN.fill(WHITE)
    title = FONT.render("Пицца добавлена в заказ!", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    back_button = Button(WIDTH // 2 - 100, 300, 200, 40, "Вернуться к заказу", action="back_to_order")
    back_button.draw()
    return [back_button]

def drink_confirmation():
    SCREEN.fill(WHITE)
    title = FONT.render("Напиток добавлен в заказ!", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    back_button = Button(WIDTH // 2 - 100, 300, 200, 40, "Вернуться к заказу", action="back_to_order")
    back_button.draw()
    return [back_button]

def display_current_order(x, y):
    total = 0
    if current_order:
        SCREEN.blit(FONT.render("Текущий заказ:", True, BLACK), (x, y))
        y += 30
        for item in current_order:
            description = item.get_description()
            SCREEN.blit(FONT.render(description, True, BLACK), (x, y))
            y += 30
            total += item.price
        SCREEN.blit(FONT.render(f"Итого: {total}", True, BLACK), (x, y))
    else:
        SCREEN.blit(FONT.render("Заказ пуст.", True, BLACK), (x, y))

# Главный цикл
running = True
while running:
    pygame.display.update()
    buttons = []

    if state == MAIN_MENU:
        buttons = main_menu()
    elif state == CATEGORY_SELECTION:
        buttons = category_selection_screen()
    elif state == ORDER_CREATION:
        buttons = order_creation_screen()
    elif state == DRINK_SELECTION:
        buttons = drink_selection_screen()
    elif state == DRINK_SIZE_SELECTION:
        buttons = drink_size_selection(selected_drink_name)
    elif state == PIZZA_SIZE_SELECTION:
        buttons = pizza_size_selection(selected_pizza_name)
    elif state == PIZZA_DOUGH_SELECTION:
        buttons = pizza_dough_selection()
    elif state == PIZZA_TOPPINGS_SELECTION:
        buttons = pizza_toppings_selection()
    elif state == PIZZA_CONFIRMATION:
        buttons = pizza_confirmation()
    elif state == DRINK_CONFIRMATION:
        buttons = drink_confirmation()
    elif state == ORDER_STATUS:
        buttons = order_status_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    action = button.action
                    if state == MAIN_MENU and action == "start_order":
                        state = CATEGORY_SELECTION
                    elif state == CATEGORY_SELECTION:
                        if action == "pizza_category":
                            state = ORDER_CREATION
                        elif action == "drink_category":
                            state = DRINK_SELECTION
                        elif action == "checkout":
                            state = ORDER_STATUS
                    elif state == ORDER_CREATION:
                        selected_pizza_name = action
                        selected_size = None
                        selected_dough = None
                        selected_toppings = []
                        state = PIZZA_SIZE_SELECTION
                    elif state == DRINK_SELECTION:
                        selected_drink_name = action
                        state = DRINK_SIZE_SELECTION
                    elif state == PIZZA_SIZE_SELECTION:
                        selected_size = action
                        state = PIZZA_DOUGH_SELECTION
                    elif state == DRINK_SIZE_SELECTION:
                        selected_drink_size = action
                        drink_price = drink_sizes[selected_drink_size]
                        drink = Drink(selected_drink_name, drink_price, selected_drink_size)
                        current_order.append(drink)
                        state = DRINK_CONFIRMATION
                    elif state == PIZZA_DOUGH_SELECTION:
                        selected_dough = action
                        state = PIZZA_TOPPINGS_SELECTION
                    elif state == PIZZA_TOPPINGS_SELECTION:
                        if action == "confirm_pizza":
                            base_price = 2000
                            total_price = base_price
                            total_price += sizes[selected_size]
                            total_price += dough_types[selected_dough]
                            for topping in selected_toppings:
                                total_price += available_toppings[topping]
                            pizza = Pizza(selected_pizza_name, total_price, selected_size, selected_dough, selected_toppings.copy())
                            current_order.append(pizza)
                            state = PIZZA_CONFIRMATION
                        else:
                            if action in selected_toppings:
                                selected_toppings.remove(action)
                            else:
                                selected_toppings.append(action)
                    elif action == "back_to_order":
                        state = CATEGORY_SELECTION
                    elif action == "back_to_category":
                        state = CATEGORY_SELECTION

pygame.quit()
sys.exit()