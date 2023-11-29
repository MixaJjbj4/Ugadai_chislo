import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import  Command,CommandStart
from aiogram.types import Message

BOT_TOKEN =

bot =Bot(BOT_TOKEN)
dp = Dispatcher
#КОЛЛИЧЕСТВО ДОСТУПНЫХ ПОПЫТОК
ATTEMPTS = 5

#Словарь, в котором будут храниться данные пользователя
user = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}

#функция для генерации случайного числа
def get_random_number() -> int:
    return random.randint(1, 100)

#Хендлер для команды start
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавай сыграй в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных'
        'команд - отправьте команду /help'
    )

# Этот хендлер ьудет срабутывать на команду '/help'
@dp.message(CommandStart(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: {user["total_games"]}/n'
        f'игр выиграно: {user["wins"]}'
    )

#Хендлер под команду '/canсel'
@dp.message(Command(command='cancel'))
async def process_cancel_command(message: Message):
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снвоа - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем.'
            'Может, сыграем разок?'
        )

# Этот хендлер будет срабатывать на согласие пользователя на игру
@dp.message(F.text.lower().in_(['Да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        await message.answer(
            'Ура\n\nЯ загадал число от 1 до 100,'
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу'
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /start'
        )

# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылаайте, '
            'пожалуйста, числа от 1 до 100'
        )


# Хендлер для обработки принятых чисел
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['total_games'] +=1
            user['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < user['secret_number']:
            user['attempts'] -=1
            await message.answer('Мое число больше')

        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {user["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


















