import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler,
    filters
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(уровень) - %(message)s', level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

TOKEN = "7016855818:AAF3avDohdL9wnUzGD6I82SNoaIYMLaX_JY"

START_ROUTES, END_ROUTES = range(2)

# Define state constants
ONE, TWO, THREE, FOUR, FIVE, MENU, MAIN_MENU = range(7)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.chat.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Привет, {first_name}! Я чат-бот Научной библиотеки РУДН. Чем могу быть полезен? Введите /menu для начала.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=(f"В данной версии бота доступны следующие команды:\n"
                                         f"/help - справка о командах\n"
                                         f"/q - задать вопрос\n"
                                         f"/feedback - оставить свои мнения и предложения по улучшению бота\n"
                                         f"/menu - менюшка"))

async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_arg = " ".join(context.args)
    answer = accresp(user_arg)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    userid = update.message.from_user.id
    addfeedback(text, userid)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Спасибо за ваше мнение!')

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Вопросы❓", "Переход на оператора📞"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите:", reply_markup=reply_markup)
    return START_ROUTES

async def handle_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["сдать книгу", "задолженность"],
        ["потерял книгу", "продлить книгу"],
        ["не успел сдать книгу", "Вернуться в меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберете вопрос про книгу:", reply_markup=reply_markup)
    return START_ROUTES

async def handle_library(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["что такое нб", "как работает библиотека"],
        ["библиотека главного корпуса", "что такое унибц"],
        ["режим работы библиотеки", "Вернуться в меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберете вопрос про библиотеку:", reply_markup=reply_markup)
    return START_ROUTES

async def handle_ud(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["удаленный доступ к", "электронную версию"],
        ["удоступ в базы", "Вернуться в меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберете вопрос про Уд:", reply_markup=reply_markup)
    return START_ROUTES

async def handle_ebs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["что такое эбс", "вход в эбс"],
        ["помощь в эбс", "Вернуться в меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберете вопрос про ЭБС:", reply_markup=reply_markup)
    return START_ROUTES

async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["подписать обходной лист", "сдать диссертацию"],
        ["место для мусульман", "зарегистрироваться в ТУИС РУДН", "Вернуться в меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберете вопрос:", reply_markup=reply_markup)
    return START_ROUTES

# Handlers for specific book questions
async def book_surrender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
    1. Библиотека в главном корпусе ул. Миклухо-Маклая, 6
        пн-чт – 11.00-17.45
        пт - 11.00-16.45
        сб - 13.00-16.45
    2. Библиотека инженерной академии и факультета физико-математических и естественных наук ул. Орджоникидзе, 3
        пн-чт – 11.00-17.45
        пт - 11.00-16.45
    3. Библиотека института русского языка, ул. Миклухо-Маклая, 10 к.2
        пн – пт 12.30 – 17.30
        """
    )
async def book_debt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Информация о выданных книгах и сроках возврата в Вашем личном кабинете. Перейдите по адресу https://lib.rudn.ru/MegaPro/Web и авторизуйтесь через PASSPORT.RUDN, где логин – корпоративная электронная почта, пароль – пароль от корпоративной электронной почты.")

async def book_lost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Обратитесь в библиотеку лично или по электронной почте library@rudn.ru. Библиотекарь подскажет, какой именно книгой необходимо заменить утерянную. Это можно сделать, в том числе, через удаленные сервисы.")

async def book_extend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Укажите свои данные: ФИО, номер студенческого билета, факультет и курс. Мы продлим книги, если это возможно. Или напишем Вам о невозможности продления.")

async def book_not_in_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("В случае нарушения сроков возврата литературы Вам необходимо как можно раньше принести книгу в библиотеку. Согласно п. 5.2 Правил пользования УНИБЦ (Научной библиотекой), пользователи несут ответственность за нарушение сроков возврата или перерегистрации литературы, и могут быть лишены права пользования ресурсами библиотеки сроком от 1 до 6 месяцев по решению администрации УНИБЦ (НБ). Отслеживать информацию о выданных книгах и сроках их возврата Вы можете в Личном кабинете библиотеки.")

# Handlers for specific library questions
async def library_nb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Научная библиотека (НБ) - это основное место хранения научной и учебной литературы в нашем университете.")

async def library_how_it_works(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
    Все отделы библиотеки работают
        пн-чт с 11.00 до 17.45
        пт с 11.00 до 16.45
        сб с 13.00 до 16.45.
        """
    )

async def library_main_building(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Все студенты и преподаватели могут брать литературу в любом отделе нашей библиотеки")

async def library_unibc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("УНИБЦ (НБ) – это Учебно-научный информационный библиотечный центр (Научная библиотека) РУДН.")

async def library_hours(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
    1. Библиотека в главном корпусе ул. Миклухо-Маклая, 6
        пн-чт – 11.00-17.45
        пт - 11.00-16.45
        сб - 13.00-16.45
    2. Библиотека инженерной академии и факультета физико-математических и естественных наук ул. Орджоникидзе, 3
        пн-чт – 11.00-17.45
        пт - 11.00-16.45
    3. Библиотека института русского языка, ул. Миклухо-Маклая, 10 к.2
        пн – пт 12.30 – 17.30
        """
    )

# Handlers for specific UD questions
async def ud_remote_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Необходимо подключить компьютер к прокси-серверу РУДН, следуя рекомендациям из инструкции для доступа к электронным ресурсам. При переходе на сайты электронных ресурсов потребуется ввести данные корпоративной почты РУДН (электронная почта должна заканчиваться на @pfur.ru).")

async def ud_electronic_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("В ЭБС РУДН в поле ПОИСК следует поставить галочку ˅ рядом с полем 'Электронная версия'.")

async def ud_database_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Для удаленного доступа необходимо подключить прокси-сервер. Инструкцию по подключению можно найти на сайте https://lib.rudn.ru")

# Handlers for specific EBS questions
async def ebs_what(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "ЭБС РУДН – это Электронно-библиотечная система РУДН. Включает учебники, учебные пособия, лабораторные практикумы, методические материалы, монографии, статьи на русском и иностранных языках в печатном и цифровом форматах, в том числе преподавателей РУДН.\n"
    "С помощью ЭБС РУДН можно произвести поиск, отбор и заказ интересующей литературы, а также просматривать личный кабинет, содержащий информацию по ранее выданным Вам книгам."
)

async def ebs_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Войдите в ЭБС РУДН https://lib.rudn.ru/MegaPro/Web и авторизуйтесь через PASSPORT.RUDN, где логин – корпоративная электронная почта, пароль – пароль от  корпоративной электронной почты.")

async def ebs_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Если у вас возникли проблемы с использованием ЭБС, пожалуйста, обратитесь в службу поддержки нашей библиотеки.")

async def other_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("На подписание обходного листа отводится 3 дня. Если нужно быстрее, то напишите на почту библиотеки library@rudn.ru")

async def other_mus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("РУДН является светским университетом, поэтому в читальных залах нет разделения по конфессиональному и гендерному принципу.")

async def other_dis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диссертация + два автореферата в фонд УНИБЦ (НБ) принимаются в рабочие дни с 10.00 до 17.45 в Отделе комплектования (главный корпус, цокольный этаж, к. 63, 64, 66 Научной библиотеки), в субботу с 13.00 до 16.45 в отделе обслуживания в главном корпусе.")

async def other_reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Авторизация в ТУИС осуществляется с помощью учетных данных от корпоративной почты РУДН. Получить их можно здесь. Войдите в корпоративную почту РУДН, затем на странице входа в ТУИС сразу нажмите на кнопку Войти с корпоративным аккаунтом.")
async def operator_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Связаться с оператором: @l3xs1s")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Вопросы❓":
        keyboard = [
            ["Книги📚", "Библиотека🏛️", "Уд📶", "Эбс🛠️"],
            ["Прочее"],
            ["Вернуться в главное меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Выберите категорию вопроса:", reply_markup=reply_markup)
        return START_ROUTES

    elif text == "Книги📚":
        return await handle_books(update, context)

    elif text == "Библиотека🏛️":
        return await handle_library(update, context)

    elif text == "Уд📶":
        return await handle_ud(update, context)

    elif text == "Эбс🛠️":
        return await handle_ebs(update, context)

    elif text == "Прочее":
        return await handle_other(update, context)

    elif text == "Переход на оператора📞":
        return await operator_transfer(update, context)

    elif text == "Вернуться в меню":
        return await main_menu(update, context)

    elif text == "Вернуться в главное меню":
        return await main_menu(update, context)


    elif text == "сдать книгу":
        return await book_surrender(update, context)
    elif text == "задолженность":
        return await book_debt(update, context)
    elif text == "потерял книгу":
        return await book_lost(update, context)
    elif text == "продлить книгу":
        return await book_extend(update, context)
    elif text == "не успел сдать книгу":
        return await book_not_in_time(update, context)


    elif text == "что такое нб":
        return await library_nb(update, context)
    elif text == "как работает библиотека":
        return await library_how_it_works(update, context)
    elif text == "библиотека главного корпуса":
        return await library_main_building(update, context)
    elif text == "что такое унибц":
        return await library_unibc(update, context)
    elif text == "режим работы библиотеки":
        return await library_hours(update, context)


    elif text == "удаленный доступ к":
        return await ud_remote_access(update, context)
    elif text == "электронную версию":
        return await ud_electronic_version(update, context)
    elif text == "удоступ в базы":
        return await ud_database_access(update, context)


    elif text == "что такое эбс":
        return await ebs_what(update, context)
    elif text == "вход в эбс":
        return await ebs_login(update, context)
    elif text == "помощь в эбс":
        return await ebs_help(update, context)

    elif text == "подписать обходной лист":
        return await other_list(update, context)
    elif text == "сдать диссертацию":
        return await other_dis(update, context)
    elif text == "место для мусульман":
        return await other_mus(update, context)
    elif text == "зарегистрироваться в ТУИС РУДН":
        return await other_reg(update, context)

    else:
        await update.message.reply_text("Пожалуйста, выберите один из доступных вариантов.")
        return START_ROUTES

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    question_handler = CommandHandler('q', question)
    feedback_handler = CommandHandler('feedback', feedback)
    help_handler = CommandHandler('help', help)
    main_menu_handler = CommandHandler('menu', main_menu)

    application.add_handler(start_handler)
    application.add_handler(question_handler)
    application.add_handler(feedback_handler)
    application.add_handler(help_handler)
    application.add_handler(main_menu_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))

    application.run_polling()

if __name__ == '__main__':
    main()
