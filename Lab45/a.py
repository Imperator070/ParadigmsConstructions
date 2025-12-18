from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Определение состояний
START, ACTION_CHOSEN, CONFIRMED = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Действие 1", callback_data='action1')],
        [InlineKeyboardButton("Действие 2", callback_data='action2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f'Привет, {user.first_name}! Выберите действие:',
        reply_markup=reply_markup
    )
    return START

async def action_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data
    context.user_data['chosen_action'] = action

    keyboard = [
        [InlineKeyboardButton("Подтвердить", callback_data='confirm')],
        [InlineKeyboardButton("Отмена", callback_data='cancel')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Вы выбрали: {action}. Подтвердить?",
        reply_markup=reply_markup
    )
    return ACTION_CHOSEN

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = context.user_data.get('chosen_action', 'неизвестно')
    await query.edit_message_text(f"Действие '{action}' выполнено!")
    return CONFIRMED

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Действие отменено.")
    return CONFIRMED

async def reset_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # После завершения возвращаем в начальное состояние
    keyboard = [
        [InlineKeyboardButton("Начать снова", callback_data='start_over')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Готово! Нажмите кнопку ниже, чтобы начать заново.", reply_markup=reply_markup)
    return CONFIRMED

def main():
    TOKEN = "YOUR_BOT_TOKEN_HERE"  # Замените на токен вашего бота
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [CallbackQueryHandler(action_chosen)],
            ACTION_CHOSEN: [
                CallbackQueryHandler(confirm, pattern='^confirm$'),
                CallbackQueryHandler(cancel, pattern='^cancel$'),
            ],
            CONFIRMED: [
                CallbackQueryHandler(start, pattern='^start_over$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, reset_to_start),
            ],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
