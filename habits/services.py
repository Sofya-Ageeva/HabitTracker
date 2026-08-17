import requests
from django.conf import settings

TELEGRAM_API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/"


def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""
    try:
        url = f"{TELEGRAM_API_URL}sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
        }
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
        return None


def format_habit_message(habit):
    """Форматирование сообщения о привычке"""
    message = (
        f"🔔 <b>Напоминание о привычке!</b>\n\n"
        f"<b>Действие:</b> {habit.action}\n"
        f"<b>Место:</b> {habit.place}\n"
        f"<b>Время:</b> {habit.time.strftime('%H:%M')}\n"
    )

    if habit.periodicity > 1:
        message += f"<b>Периодичность:</b> раз в {habit.periodicity} дн.\n"

    if habit.reward:
        message += f"<b>Вознаграждение:</b> {habit.reward}\n"

    if habit.related_habit:
        message += f"<b>Связанная привычка:</b> {habit.related_habit.action}\n"

    return message