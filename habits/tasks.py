from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from .services import send_telegram_message, format_habit_message


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках"""
    now = timezone.now()
    current_time = now.time()
    current_date = now.date()

    habits = Habit.objects.filter(
        is_active=True,
        time__lte=current_time,
    )

    sent_count = 0
    for habit in habits:
        last_sent = getattr(habit, 'last_reminder_sent', None)

        if last_sent:
            days_since = (current_date - last_sent).days
            if days_since < habit.periodicity:
                continue

        if habit.user.telegram_chat_id:
            message = format_habit_message(habit)
            send_telegram_message(habit.user.telegram_chat_id, message)

            habit.last_reminder_sent = current_date
            habit.save(update_fields=['last_reminder_sent'])
            sent_count += 1

    return f"Отправлено {sent_count} напоминаний"


@shared_task
def send_test_telegram_message(chat_id):
    """Тестовая задача для проверки Telegram"""
    message = "<b>Тестовое сообщение!</b>\n\nРаботает!"
    return send_telegram_message(chat_id, message)