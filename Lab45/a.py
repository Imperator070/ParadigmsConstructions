import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Данные вопросов
TOPICS = {
    "math": [
        {
            "question": "Сколько будет 2+2?",
            "options": ["3", "4", "5"],
            "correct": 1
        },
        {
            "question": "Квадратный корень из 16?",
            "options": ["2", "4", "8"],
            "correct": 1
        }
    ],
    "history": [
        {
            "question": "В каком году началась Вторая мировая война?",
            "options": ["1939", "1941", "1914"],
            "correct": 0
        },
        {
            "question": "Кто был первым президентом США?",
            "options": ["Томас Джефферсон", "Джордж Вашингтон", "Авраам Линкольн"],
            "correct": 1
        }
    ]
}

# Состояния конечного автомата
STATE_START = "start"
STATE_QUESTION = "question"
STATE_ANSWER = "answer"

# Хранение состояний пользователей
user_states = {}
user_data = {}  # Для хранения текущей темы и вопроса

def start(update: Update, context: CallbackContext) -> None:
    """Начало работы с ботом"""
    user_id = update.message.from_user.id
    user_states[user_id] = STATE_START

    keyboard = [
        [InlineKeyboardButton("Математика", callback_data="math")],
        [InlineKeyboardButton("История", callback_data="history")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "📚 Добро пожаловать в режим подготовки к экзамену!\n"
        "Выберите тему, чтобы начать:",
        reply_markup=reply_markup
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    data = query.data

    # Обработка команды перезапуска
    if data == "restart":
        user_states[user_id] = STATE_START
        keyboard = [
            [InlineKeyboardButton("Математика", callback_data="math")],
            [InlineKeyboardButton("История", callback_data="history")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            "Выберите следующую тему:",
            reply_markup=reply_markup
        )
        return

    current_state = user_states.get(user_id, STATE_START)

    # Состояние выбора темы
    if current_state == STATE_START:
        topic = data
        user_data[user_id] = {"topic": topic}

        # Случайный выбор вопроса
        questions = TOPICS[topic]
        question_idx = random.randint(0, len(questions) - 1)
        user_data[user_id]["question_idx"] = question_idx
        question = questions[question_idx]

        # Формирование кнопок с вариантами ответов
        keyboard = [
            [InlineKeyboardButton(option, callback_data=f"ans_{idx}")]
            for idx, option in enumerate(question["options"])
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            text=f"❓ Вопрос по теме '{topic}':\n\n{question['question']}",
            reply_markup=reply_markup
        )
        user_states[user_id] = STATE_QUESTION

    # Состояние ответа на вопрос
    elif current_state == STATE_QUESTION:
        selected_idx = int(data.split("_")[1])
        topic = user_data[user_id]["topic"]
        question_idx = user_data[user_id]["question_idx"]
        question = TOPICS[topic][question_idx]

        # Проверка ответа
        is_correct = (selected_idx == question["correct"])
        result_text = "✅ Правильно!" if is_correct else f"❌ Неверно. Правильный ответ: {question['options'][question['correct']]}"

        # Отправка результата
        query.edit_message_text(
            text=f"{result_text}\n\n{question['question']}\nВаш ответ: {question['options'][selected_idx]}"
        )

        # Кнопка для продолжения
        keyboard = [[InlineKeyboardButton("Следующий вопрос ➡️", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(
            chat_id=user_id,
            text="📊 Результат проверен. Хотите продолжить?",
            reply_markup=reply_markup
        )
        user_states[user_id] = STATE_ANSWER

def main() -> None:
    """Основная функция запуска бота"""
    # Замените 'YOUR_TOKEN' на токен вашего бота
    updater = Updater("YOUR_TOKEN")
    dispatcher = updater.dispatcher

    # Регистрация обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # Запуск бота
    updater.start_polling()
    logging.info("Бот запущен и готов к работе")
    updater.idle()

if __name__ == "__main__":
    main()
