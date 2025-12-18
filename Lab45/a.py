import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Замените на ваш токен
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение состояний FSM
class ExamStates(StatesGroup):
    initial = State()         # Начальное состояние
    topic_selection = State() # Выбор темы
    answering = State()       # Ответ на вопрос

# База вопросов
questions_db = {
    "Математика": {
        "question": "Сколько будет 2+2*2?",
        "options": ["4", "6", "8"],
        "correct": "6"
    },
    "Физика": {
        "question": "Чему равно ускорение свободного падения на Земле?",
        "options": ["9.8 м/с²", "10 м/с²", "8.9 м/с²"],
        "correct": "9.8 м/с²"
    },
    "Информатика": {
        "question": "Сколько бит в одном байте?",
        "options": ["4", "8", "16"],
        "correct": "8"
    }
}

# Обработчик команды /start
@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📚 Начать подготовку")

    await message.answer(
        "🎓 Привет! Я помогу тебе подготовиться к экзамену.\n"
        "Нажми кнопку ниже, чтобы начать:",
        reply_markup=keyboard
    )
    await ExamStates.initial.set()

# Начальное состояние
@dp.message_handler(state=ExamStates.initial)
async def process_initial(message: types.Message, state: FSMContext):
    if message.text == "📚 Начать подготовку":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*questions_db.keys())

        await message.answer(
            "📘 Выбери тему для подготовки:",
            reply_markup=keyboard
        )
        await ExamStates.topic_selection.set()
    else:
        await message.answer("Пожалуйста, используй кнопки внизу экрана")

# Выбор темы
@dp.message_handler(state=ExamStates.topic_selection)
async def process_topic_selection(message: types.Message, state: FSMContext):
    selected_topic = message.text

    if selected_topic not in questions_db:
        await message.answer("Пожалуйста, выбери тему из предложенных")
        return

    # Сохраняем выбранную тему
    await state.update_data(topic=selected_topic)

    # Готовим вопрос
    question_data = questions_db[selected_topic]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*question_data["options"])

    await message.answer(
        f"❓ Вопрос по теме '{selected_topic}':\n\n{question_data['question']}",
        reply_markup=keyboard
    )
    await ExamStates.answering.set()

# Обработка ответа
@dp.message_handler(state=ExamStates.answering)
async def process_answer(message: types.Message, state: FSMContext):
    user_answer = message.text
    data = await state.get_data()
    topic = data['topic']
    correct_answer = questions_db[topic]['correct']

    # Готовим клавиатуру для продолжения
    continue_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    continue_keyboard.add("📚 Выбрать другую тему", "🏠 Вернуться в меню")

    # Проверяем ответ
    if user_answer == correct_answer:
        await message.answer(
            "✅ Правильно! Отлично разбираешься в теме!",
            reply_markup=continue_keyboard
        )
    else:
        await message.answer(
            f"❌ Неверно. Правильный ответ: {correct_answer}\n"
            "Не расстраивайся, попробуй другую тему!",
            reply_markup=continue_keyboard
        )

    # Ожидаем дальнейших действий
    await ExamStates.initial.set()

# Обработчик для возврата в меню
@dp.message_handler(state=ExamStates.initial)
async def process_menu_selection(message: types.Message, state: FSMContext):
    if message.text == "📚 Выбрать другую тему":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*questions_db.keys())

        await message.answer("📘 Выбери новую тему:", reply_markup=keyboard)
        await ExamStates.topic_selection.set()

    elif message.text == "🏠 Вернуться в меню":
        start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_keyboard.add("📚 Начать подготовку")

        await message.answer(
            "🎓 Главное меню. Нажми кнопку ниже для продолжения:",
            reply_markup=start_keyboard
        )
    else:
        await message.answer("Пожалуйста, используй кнопки внизу экрана")

# Обработчик по умолчанию
@dp.message_handler()
async def default_handler(message: types.Message):
    await cmd_start(message, None)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
