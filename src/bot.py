from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import asyncio

# Пример списка анекдотов
jokes = [    
    "Заходит Паскаль в бар, а в баре сто тысяч паскалей...",
    "Про могилу: — Почему нельзя спрятать тайну на кладбище? — Потому что все там мертвы и выкопаны (pun on \"grave\" as serious).",
    "Почему программисты не могут покататься на скейтборде? Потому что они боятся, что будут зацеплены за баг.",
    "Какой самый оптимистичный язык программирования? Python, потому что он просто не может быть неудачным.",
    "Почему JavaScript такие бедные? Потому что они всегда тратят всё на 'this'.",
    "Какой язык программирования самый красивый? С++, потому что у него самые красивые 'скобочки'.",
    "Про фотоны: — Почему фотону не нужен чемодан? — Потому что у него нет массы.",    
    "Про нейтроны: — Нейтрон заходит в бар и спрашивает: «Сколько стоит выпивка?» Бармен отвечает: «Для вас — бесплатно. Никакого заряда!»",
    "Про химическую реакцию: — Два атома гуляют по улице. Один вдруг говорит: «Ой, я потерял электрон!» Второй спрашивает: «Ты уверен?»  — «Да, я положительно заряжен!»",
    "Про кота Шрёдингера: — Что сказал кот Шрёдингера, когда попал в коробку? — «Я жив… или нет».",
    "Про кислород и калий: — Что произойдет, если объединить кислород и калий?  — Получится \"ОК\"!",
    "Про математику: — Почему математики не ходят на вечеринки? — Потому что вероятность веселья стремится к нулю.",
    "Про энтропию: — Почему никто не любит обсуждать энтропию? — Потому что разговоры сразу скатываются в хаос.",
    "Про химические элементы: — Почему гелий, неон и аргон никогда не участвуют в вечеринках? — Потому что они все благородные газы!",
    "Про ускорение: — Ускорение и скорость зашли в бар. Ускорение разливает напитки и говорит: «Расслабься, это только начало».",
    "Почему программисты любят кофе? Потому что он помогает им не 'пить' баги!"
]

# Примеры смайлов
smileys = ["😊", "😂", "👻", "🕷️", "😎", "😜", "😁", "💀", "😅", "😋"]


def get_joke():
    return random.choice(jokes)

def get_random_smileys():
    return ''.join(random.choice(smileys) for _ in range(random.randint(4, 7)))

async def start(update: Update, context: CallbackContext) -> None:
    print("Получена команда /start")  # Отладочное сообщение
    
    # Отправляем начальное сообщение с кнопкой
    keyboard = [[InlineKeyboardButton("Получить свежий анекдот", callback_data='new_joke')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await update.message.reply_text("Нажми, чтобы получить анекдот", reply_markup=reply_markup)
    
    # Сохраняем ID сообщения с кнопкой
    context.user_data['message_ids'] = [message.message_id]

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    print("Получен запрос на кнопку")  # Отладочное сообщение

    if query.data == 'new_joke':
        joke = get_joke()
        print(f"Отправляем анекдот: {joke}")  # Отладочное сообщение
        
        # Сохраняем старый анекдот для сдвига
        if 'message_ids' in context.user_data:
            previous_message_id = context.user_data['message_ids'][-1]
            try:
                # Отправляем смайлики для сдвига старого анекдота вниз
                for _ in range(1):  # Отправляем три сообщения со смайликами
                    await asyncio.sleep(0.5)  # Задержка перед отправкой
                    smileys_message = get_random_smileys()
                    await query.message.edit_text(smileys_message)  # Обновляем текст сообщения

                # Удаляем старое сообщение с кнопкой и смайлами
                await asyncio.sleep(1)  # Задержка перед удалением старого сообщения
                await context.bot.delete_message(chat_id=query.message.chat_id, message_id=previous_message_id)
            except Exception as e:
                print(f"Не удалось удалить старое сообщение: {e}")

        # Отправляем новый анекдот и кнопку
        keyboard = [[InlineKeyboardButton("Получить свежий анекдот", callback_data='new_joke')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        new_message = await query.message.reply_text(joke, reply_markup=reply_markup)
        
        # Сохраняем ID нового сообщения
        context.user_data['message_ids'].append(new_message.message_id)

def main():
    application = Application.builder().token("token").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    print("Бот запущен")  # Отладочное сообщение
    application.run_polling()

if __name__ == '__main__':
    main()
