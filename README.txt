Sweetly
======

Sweetly — це невеликий інтернет‑магазин десертів на Django з авторизацією, кошиком, оформленням замовлення та оплатою через Stripe.

Технології
---------

- Python / Django (бекенд, ORM, маршрути)
- django‑allauth (реєстрація та логін)
- django‑axes (захист від перебору паролів)
- Stripe (оплати)
- Bootstrap 5 (інтерфейс)
- python‑dotenv (налаштування через `.env`)

Локальний запуск
----------------

1. Клонувати репозиторій:

   python -m venv .venv
   .venv\Scripts\activate  # Windows

2. Встановити залежності (мінімальний набір):

   pip install django django-allauth django-axes stripe python-dotenv django-debug-toolbar

3. Створити файл `.env` у корені проєкту з основними змінними:

   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...

   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password
   DEFAULT_FROM_EMAIL="Sweetly <noreply@sweetly.ua>"

4. Виконати міграції та запустити сервер:

   python manage.py migrate
   python manage.py createsuperuser  # за бажанням
   python manage.py runserver

Тести
-----

Тести розкладені по додатках у файлах `tests.py`:

- core — головна, «Про нас», «Доставка», кеш популярних товарів
- catalog — моделі та списки/деталі товарів, автодоповнення пошуку
- cart — логіка кошика та JSON‑ендпоінти
- orders — моделі замовлень та історія замовлень
- payments — сторінка успішної оплати
- accounts — сторінки реєстрації, логіну та профілю

Запустити всі тести:

   python manage.py test

