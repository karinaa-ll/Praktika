##"Крестики-нолики"

# import os

# # Цвета ANSI
# RED = '\033[94m'
# BLUE = '\033[91m' 
# RESET = '\033[0m'

# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')

# def colored(symbol):
#     if symbol == 'X':
#         return BLUE + 'X' + RESET
#     elif symbol == 'O':
#         return RED + 'O' + RESET
#     return symbol

# def print_field(field):
#     print()
#     for i in range(3):
#         row = [colored(field[3*i + j]) for j in range(3)]
#         print(f" {row[0]} | {row[1]} | {row[2]}")
#         if i < 2:
#             print("---|---|---")
#     print()

# def check_win(field, symbol):
#     win_combinations = [
#         [0, 1, 2], [3, 4, 5], [6, 7, 8],
#         [0, 3, 6], [1, 4, 7], [2, 5, 8],
#         [0, 4, 8], [2, 4, 6]
#     ]
#     return any(all(field[i] == symbol for i in combo) for combo in win_combinations)

# def is_draw(field):
#     return all(cell in ['X', 'O'] for cell in field)

# def play_game():
#     while True:
#         field = [str(i) for i in range(1, 10)]
#         current_player = 'X'
#         game_over = False

#         while not game_over:
#             clear_screen()
#             print_field(field)
#             try:
#                 move = int(input(f"Ход игрока {current_player}. Введите номер клетки (1-9): "))
#                 if move < 1 or move > 9:
#                     print("Ошибка: введите число от 1 до 9.")
#                     continue
#                 if field[move - 1] in ['X', 'O']:
#                     print("Ошибка: клетка уже занята.")
#                     continue
#                 field[move - 1] = current_player
#                 if check_win(field, current_player):
#                     clear_screen()
#                     print_field(field)
#                     print(f"Победил игрок {colored(current_player)}!\n")
#                     game_over = True
#                 elif is_draw(field):
#                     clear_screen()
#                     print_field(field)
#                     print("Ничья!\n")
#                     game_over = True
#                 else:
#                     current_player = 'O' if current_player == 'X' else 'X'
#             except ValueError:
#                 print("Ошибка: введите корректное число.")

#         again = input("Сыграть ещё раз? (Y/N): ").strip().upper()
#         if again != 'Y':
#             print("Спасибо за игру!")
#             break


# play_game()




#"Битва с монстром"


import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Character:
    def __init__(self, name, health, attack, defence):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence

    def is_alive(self):
        return self.health > 0

    def attack_target(self, other):
        damage = max(0, self.attack - other.defence + random.randint(-2, 2))
        other.health -= damage
        other.health = max(0, other.health)
        print(f"{self.name} атакует {other.name} и наносит {damage} урона!")

def print_status(hero, monster):
    print("\n===== СТАТУС =====")
    print(f"{hero.name} — ❤️ {hero.health}, 🗡️ {hero.attack}, 🛡️ {hero.defence}")
    print(f"{monster.name} — ❤️ {monster.health}, 🗡️ {monster.attack}, 🛡️ {monster.defence}")
    print("===================\n")

def player_turn(player, enemy):
    while True:
        print("1. Атаковать")
        print("2. Пропустить ход")
        choice = input("Выберите действие (1/2): ").strip()
        if choice == '1':
            player.attack_target(enemy)
            break
        elif choice == '2':
            print(f"{player.name} пропускает ход.")
            break
        else:
            print("Неверный ввод. Введите 1 или 2.")

def monster_turn(monster, player):
    action = random.choice(['attack', 'skip'])
    if action == 'attack':
        monster.attack_target(player)
    else:
        print(f"{monster.name} зевает и пропускает ход.")

def play_game():
    while True:
        clear_screen()
        hero = Character("Герой", health=30, attack=10, defence=5)
        monster = Character("Монстр", health=25, attack=8, defence=3)

        print("🌟 Добро пожаловать в игру 'Битва с монстром'! 🌟")
        input("Нажмите Enter, чтобы начать бой...")

        while hero.is_alive() and monster.is_alive():
            clear_screen()
            print_status(hero, monster)
            player_turn(hero, monster)
            if monster.is_alive():
                monster_turn(monster, hero)

        clear_screen()
        print_status(hero, monster)
        if hero.is_alive():
            print("🎉 Победа! Вы победили монстра!")
        else:
            print("💀 Поражение! Монстр оказался сильнее...")

        again = input("\nСыграть ещё раз? (Y/N): ").strip().lower()
        if again != 'y':
            print("Спасибо за игру!")
            break


play_game()
