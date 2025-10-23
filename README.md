# 🔒️ Parse blocked sites

**Parse blocked sites** — мікросервіс на основі FastAPI для парсингу публічної інформації про заблоковані домени.  
Заблоковані домени у базі даних PostgreSQL, оновлюються автоматично за допомогою Celery.

---

## 🚀 Можливості
- ⏱ Кожних 30 хв. оновлюються дані по заблокованим доменам
- 🗂 Зберігання нових заблокованих доменів та видалення розблокованих. Легкий інтерфейс пошуку домена за його імям чи ip адресою
- 📋 Генерація файлу ексель збережених даних
- 📊 Статистика парсингу заблокованих доменів
- 🐘 Використання PostgreSQL для зберігання  
- 🟢 Підтримка Celery + Redis для асинхронних задач з інтегрованим логуванням 
- 🐳 Готовий для запуску у Docker / Docker Compose  

---

## 🛠️ Технології
- [FastAPI](https://fastapi.tiangolo.com/) — бекенд  
- [SQLAlchemy + Alembic](https://www.sqlalchemy.org/) — ORM та міграції  
- [Pydantic](https://docs.pydantic.dev/) — валідація даних  
- [Celery](https://docs.celeryq.dev/) — асинхронні задачі  
- [Redis](https://redis.io/) — брокер для Celery  
- [PostgreSQL](https://www.postgresql.org/) — основна база даних 
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - парсер
- [Docker](https://www.docker.com/) — контейнеризація  

---

## ⚙️ Запуск через Docker
> Попередньо переконайся, що у тебе встановлено **Docker** та **Docker Compose**.

### Клонування репозиторію
```bash
git clone git@github.com:Igor-Cegelnyk/parse-blocked-sites.git
cd parse-blocked-sites
```

### Створення файлу .env (якщо його ще немає)
```bash
touch .env
```

### Відкрий .env у будь-якому редакторі
```bash
nano .env 
```

### 📋 Структура .env

```angular2html
# Налаштування сервера
APP_CONFIG__RUN__HOST=0.0.0.0
APP_CONFIG__RUN__PORT=8001
# Налаштування Redis
APP_CONFIG__REDIS__HOST=redis
APP_CONFIG__REDIS__PORT=6379
APP_CONFIG__REDIS__EXPIRES=36000
# Налаштування DB
APP_CONFIG__DB__USER=
APP_CONFIG__DB__PASSWORD=
APP_CONFIG__DB__DB_NAME=blocked_sites
APP_CONFIG__DB__PORT=5432
APP_CONFIG__DB__HOST=pg
# Налаштування парсера
APP_CONFIG__BASE_URL=
APP_CONFIG__API_URL=
```

### 🌐 Веб-інтерфейс

👉 http://localhost:8001


### 📘 API Документація

👉 http://localhost:8001/docs

## 📊 Моніторинг задач (Flower)

Для зручного контролю стану Celery є веб-інтерфейс:  

📍 [http://localhost:5555](http://0.0.0.0:5555)  

Там можна переглянути:
- чергу задач  
- статус виконання  
- історію запусків  
- логування помилок  

## 🔑 Налаштування

Всі параметри конфігурації беруться з **.env** файлу для тестування
