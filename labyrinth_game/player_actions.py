from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state: dict):
    """
    Ф-ция для просмотра инвентаря пользователя
    :param game_state:
    :return:
    """
    if not game_state.get('player_inventory'):
        print('Ваш инвентарь пуст')
    else:
        print(game_state.get('player_inventory'))

def move_player(game_state: dict, direction: str):
    current_room = game_state.get('current_room')
    exits = ROOMS[current_room]['exits']

    if direction not in exits:
        print('Нельзя пойти в этом направлении.')
        return
    next_room = exits[direction]

    if next_room == "treasure_room":
        if 'rusty_key' in game_state['player_inventory']:
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.") # noqa: E501
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state['current_room'] = next_room
    game_state['steps_taken'] += 1
    random_event(game_state)
    describe_current_room(game_state)


def take_item(game_state:dict, item_name:str):
    current_room = game_state.get('current_room')
    items = ROOMS[current_room]['items']

    if item_name not in items:
        print('Такого предмета здесь нет.')
        return
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    game_state['player_inventory'].append(item_name)
    ROOMS[current_room]['items'].remove(item_name)
    print(f'Вы подняли: {item_name}')


def use_item(game_state: dict, item_name:str):
    if item_name not in game_state.get('player_inventory'):
        print("У вас нет такого предмета")
        return
    match item_name:
        case 'torch':
            print("Вокруг стало светлее, благодаря факелу")
        case 'sword':
            print("Вы стали чувствовать себя уверенне с мечом в руках")
        case 'bronze_box':
            print("Вы открываете шкатулки и получаете rusty_key")
            if 'rusty_key' not in game_state.get('player_inventory'):
                game_state['player_inventory'].append('rusty_key')
        case _:
            print("Вы не знаете как использовать данный предмет")