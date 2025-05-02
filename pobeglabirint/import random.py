import random

class Player:
    def __init__(self):
        self.x = 0  # Начальная позиция игрока
        self.y = 0
        self.health = 100  # Начальное здоровье игрока

    def move(self, direction):
        if direction == 'w':  # Вверх
            self.x -= 1
        elif direction == 's':  # Вниз
            self.x += 1
        elif direction == 'a':  # Влево
            self.y -= 1
        elif direction == 'd':  # Вправо
            self.y += 1


class Enemy:
    def __init__(self):
        self.x = random.randint(0, 4)  # Случайная начальная позиция врага
        self.y = random.randint(0, 4)

    def move(self):
        direction = random.choice(['w', 's', 'a', 'd'])  # Случайный выбор направления
        if direction == 'w':  # Вверх
            if self.x > 0:
                self.x -= 1
        elif direction == 's':  # Вниз
            if self.x < 4:
                self.x += 1
        elif direction == 'a':  # Влево
            if self.y > 0:
                self.y -= 1
        elif direction == 'd':  # Вправо
            if self.y < 4:
                self.y += 1


def generate_field():
    field = [['.' for _ in range(5)] for _ in range(5)]
    # Размещение выходной клетки
    field[4][4] = 'X'

    # Размещение стенок (блокирует путь)
    wall_count = random.randint(5, 8)  # Случайное количество стен
    walls_placed = 0
    while walls_placed < wall_count:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if field[x][y] == '.' and (x != 0 or y != 0) and (x != 4 or y != 4):  # Не ставим стены в стартовую и выходную позицию
            field[x][y] = '#'
            walls_placed += 1

    # Размещение ловушек
    trap_count = random.randint(3, 5)
    traps_placed = 0
    while traps_placed < trap_count:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if field[x][y] == '.':
            field[x][y] = 'T'
            traps_placed += 1

    # Размещение зелий
    potion_count = random.randint(1, 3)
    potions_placed = 0
    while potions_placed < potion_count:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if field[x][y] == '.':
            field[x][y] = 'P'  # 'P' — это зелье
            potions_placed += 1

    return field


def print_field(field, player, enemy):
    field_copy = [row[:] for row in field]
    field_copy[player.x][player.y] = 'P'  # Обновляем позицию игрока
    field_copy[enemy.x][enemy.y] = 'E'  # Обновляем позицию врага
    for row in field_copy:
        print(' '.join(row))


def game():
    while True:
        # Инициализация игрока и врага
        player = Player()
        enemy = Enemy()
        field = generate_field()

        while player.health > 0:
            print_field(field, player, enemy)
            print(f'Здоровье: {player.health}')

            # Ввод команды движения
            move = input("Введите команду (w - вверх, s - вниз, a - влево, d - вправо): ").lower()

            # Проверка на корректность ввода
            if move not in ['w', 'a', 's', 'd']:
                print("Неверная команда! Пожалуйста, используйте w, a, s, или d.")
                continue

            # Перемещаем игрока
            player.move(move)

            # Проверка выхода за границы
            if player.x < 0 or player.x >= 5 or player.y < 0 or player.y >= 5:
                print("Вы вышли за границы поля!")
                # Возвращаем игрока на начальную позицию
                player.x = 0
                player.y = 0
                continue

            # Проверка на стенку
            if field[player.x][player.y] == '#':
                print("Вы столкнулись со стеной! Попробуйте снова.")
                # Возвращаем игрока на начальную позицию
                player.x = 0
                player.y = 0
                continue

            # Проверка на ловушку
            if field[player.x][player.y] == 'T':
                player.health -= 10  # Потеря здоровья
                print("Вы попали в ловушку! Здоровье уменьшилось на 10.")

            # Проверка на столкновение с врагом
            if player.x == enemy.x and player.y == enemy.y:
                player.health -= 20  # Потеря здоровья при столкновении
                print("Вы столкнулись с врагом! Здоровье уменьшилось на 20.")

            # Проверка на зелье
            if field[player.x][player.y] == 'P':
                player.health += 20  # Восстановление здоровья
                print("Вы нашли зелье! Здоровье увеличилось на 20.")

            # Проверка на выход
            if field[player.x][player.y] == 'X':
                print_field(field, player, enemy)
                print("Поздравляем! Вы победили!")
                break

            # Проверка на смерть
            if player.health <= 0:
                print("Ваше здоровье истощилось! Игра окончена.")
                break

            # Враг двигается
            enemy.move()

        # Повтор игры
        play_again = input("Хотите сыграть снова? (y/n): ").lower()
        if play_again != 'y':
            print("Спасибо за игру!")
            break


# Запуск игры
game()
