import math

from labyrinth_game.constants import ROOMS


def get_input(prompt="> "):
    """
    Ф-ция для ввода значений пользователем
    :param prompt:
    :return:
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def describe_current_room(game_state:dict):
    """
    Ф-ция описывает комнату в которой находится игрок
    """
    current_room = ROOMS[game_state["current_room"]]

    print(f"=={game_state.get('current_room').upper()}==")
    print(current_room.get('description'))
    print(f"Заметные предметы: {', '.join(current_room.get('items'))}")
    print(f"Выходы: {', '.join(current_room.get('exits'))}")
    if current_room.get('puzzle') is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state:dict):
    """
    Ф-ция используется для решения головоломок, которые находятся в комнате
    """
    current_room = ROOMS[game_state["current_room"]]
    puzzle = current_room.get('puzzle')

    if not puzzle:
        print("Здесь нет загадок")
        return
    question, answers = puzzle

    if isinstance(answers, str):
        answers = [answers.lower()]
    else:
        answers = [a.lower() for a in answers]

    print(question)
    while True:
        answer = get_input("Ваш ответ: ").lower()

        if answer in answers:
            print("Абсолютно верно!")
            current_room['puzzle'] = None

            for item in current_room.get('items'):
                if item not in game_state['player_inventory']:
                    game_state['player_inventory'].append(item)
                    current_room['items'].remove(item)
            return
        else:
            print("Неверно. Попробуйте снова")
            if game_state['current_room'] == "trap_room":
                trigger_trap(game_state)

def attempt_open_treasure(game_state:dict):
    """
    Ф-ция используется для попытки открыть treasure_chest
    Открытие которого приведет к победе
    """
    current_room = game_state["current_room"]

    if current_room != 'treasure_room':
        print("Здесь нет сундука, который можно открыть")
        return

    if "treasure_chest" not in ROOMS[current_room]["items"]:
        print("Сундук уже открыт или его здесь нет")
        return

    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS[current_room]['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили")
        game_state['game_over'] = True
    else:
        print("Сундук заперт. Хочешь ли ввести код? (да/нет)")
        while True:
            answer_choice = get_input("Ввод: ").lower()
            if answer_choice == 'нет':
                print("Вы отступаете от сундука.")
                return
            elif answer_choice == 'да':
                break
            else:
                print("Неизвестная команда")

        puzzle = ROOMS[current_room]['puzzle']
        if not puzzle:
            print("На сундуке нет замочной скважины или кода. Похоже нужен ключ")
            return

        question, answers = puzzle
        if isinstance(answers, str):
            answers = [answers.lower()]
        else:
            answers = [a.lower() for a in answers]

        print(question)
        answer = get_input("Ваш ответ: ").strip().lower()

        if answer in answers:
            print("Замок щёлкает! Сундук открыт!")
            ROOMS[current_room]['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
        else:
            print("Неверный код. Сундук остаётся запертым.")

# labyrinth_game/utils.py
def show_help(commands):
    """
    Используется для вывода команд игры
    """
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        # выравниваем команды слева, заполняем пробелами до 16 символов
        print(f"  {cmd:<16} - {desc}")

def pseudo_random(seed:int, modulo:int):
    """
    Ф-ция добавляет элемент случайности в игру
    """
    FIRST_NUM = 12.9891
    SECOND_NUM = 43758.5453
    prep = math.sin(seed * FIRST_NUM) * SECOND_NUM
    result = prep - math.floor(prep)
    final = int(result * modulo)
    return final


def trigger_trap(game_state:dict):
    """
    Ф-ция активирует ловушку
    """
    print("Ловушка активирована! Пол стал дрожать...")
    if not game_state.get('player_inventory'):
        if pseudo_random(0, 9) < 3:
            print("Вы проиграли, получив урон. Игра окончена")
            game_state['game_over'] = True
        else:
            print("Вам удалось уцелеть")
    else:
        i = pseudo_random(0,len(game_state['player_inventory']))
        lost_item = game_state['player_inventory'].pop(i)
        print(f"Вы потеряли {lost_item}")

def random_event(game_state:dict):
    """
    Ф-ция используется для добавления рандома в игру
    """
    SEED = game_state['steps_taken']
    if pseudo_random(SEED,10) != 1:
        return
    else:
        result = pseudo_random(SEED, 3)
        inventory = game_state['player_inventory']
        match result:
            case 0:
                print("Вы находите на полу монетку")
                ROOMS[game_state['current_room']]['items'].append('coin')
            case 1:
                print("Вы слышите шорох")
                if "sword" in inventory:
                    print("Вы отпугнули существо")
                else:
                    print("Вы испуганы")
            case 2:
                if game_state.get('current_room') == "trap_room" and "torch" not in inventory: # noqa: E501
                    print("Вы чувствуете опасность")
                    trigger_trap(game_state)
                    return