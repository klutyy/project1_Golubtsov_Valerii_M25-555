# labyrinth_game/constants.py
ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом. На полу лежит старый факел.', # noqa: E501
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.', # noqa: E501
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': ('На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.', ['10','десять']) # noqa: E501
    },
    'trap_room': {
          'description': 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".', # noqa: E501
          'exits': {'west': 'entrance'},
          'items': ['rusty_key'],
          'puzzle': ('Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")', 'шаг шаг шаг') # noqa: E501
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.', # noqa: E501
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient_book'],
          'puzzle': ('В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)', 'резонанс') # noqa: E501
    },
    'armory': {
          'description': 'Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.', # noqa: E501
          'exits': {'south': 'library','east': 'garden'},
          'items': ['sword', 'bronze_box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': 'Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.', # noqa: E501
          'exits': {'south': 'hall'},
          'items': ['treasure_chest'],
          'puzzle': ('Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? )', ['10','десять']) # noqa: E501
    },
    'garden': {
        'description': 'Заросший сад с фонтаном. Между камней блестит небольшой амулет',
        'exits': {'west': 'armory', 'north': 'secret_tunnel'},
        'items': ['amulet'],
        'puzzle': ('На стене у фонтана надпись: "Назови цвет чистой воды."', 'голубой')
    },
    'secret_tunnel': {
        'description': 'Тёмный подземный туннель. Слышен слабый сквозняк — где-то впереди выход.', # noqa: E501
        'exits': {'south': 'garden'},
        'items': ['broken_lantern','treasure_key'],
        'puzzle': None
    }
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}