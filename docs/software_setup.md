# Настройка программной части

## 1. Клонирование репозитория

```bash
git clone https://github.com/Dugtai/microclimate.git
cd microclimate
```

## 2. Создание виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 4. Настройка переменных окружения

```bash
cp .env.example .env
nano .env
```

В файл `.env` необходимо добавить реальные токены:

```env
BOT_TOKEN=telegram_bot_token_here
VK_TOKEN=vk_group_token_here
```

Файл `.env` не должен попадать в публичный репозиторий.

## 5. Проверка Telegram-бота

```bash
python src/telegram_bot.py
```

После запуска в Telegram доступны команды:

```text
/start
/help
/status
```

## 6. Проверка VK-бота

```bash
python src/vk_bot.py
```

В сообщениях VK доступны команды:

```text
статус
помощь
```

## 7. Установка systemd-сервисов

Пример для Telegram-бота:

```bash
sudo cp systemd/microclimate-telegram-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable microclimate-telegram-bot.service
sudo systemctl start microclimate-telegram-bot.service
```

Проверка статуса:

```bash
sudo systemctl status microclimate-telegram-bot.service
```

Просмотр логов:

```bash
journalctl -u microclimate-telegram-bot.service -n 100 --no-pager
```

Аналогично можно установить сервис VK-бота.
