#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    get_input,
    show_help,
    solve_puzzle,
)

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}

def process_command(game_state: dict, command_input: str):
    """
    Ф-ция для обработки команд введенных пользователем
    """
    parts = command_input.split()
    if not parts:
        print("Введите команду")
        return

    command = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    directions = {"north", "south", "east", "west"}
    if command in directions:
        move_player(game_state, command)
        return

    match command:
        case 'go':
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление (например, 'go north'")
        case 'take':
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет, который хотите взять")
        case 'inventory':
            show_inventory(game_state)
        case 'look':
            describe_current_room(game_state)
        case 'inventory' | 'show_inventory':
            show_inventory(game_state)
        case 'help' | 'show_help':
            show_help(COMMANDS)
        case 'use':
            use_item(game_state, arg)
        case 'solve':
            if game_state['current_room'] == "treasure_room":
                attempt_open_treasure(game_state)
                if game_state.get("game_over"):
                    print("Вы выиграли")
                return
            else:
                solve_puzzle(game_state)
        case 'exit' | 'quit':
            print("Выход из игры")
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда, попробуйте снова")


def main():
    """
    Основная ф-ция игры
    """
    print("Добро пожаловать в Лабиринт Сокровищ!")
    describe_current_room(game_state)

    while not game_state.get('game_over'):
        command_input = get_input("> ")

        if command_input.lower() in ("quit","exit"):
            print("Выход из игры")
            game_state['game_over'] = True
            break

        process_command(game_state, command_input)


if __name__ == "__main__":
    main()
