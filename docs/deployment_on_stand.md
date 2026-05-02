# Развёртывание на реальном стенде NanoPi-AR

Документ описывает общий порядок переноса публичной версии проекта на реальный стенд.

## 1. Клонирование проекта

```bash
cd /home/root
git clone https://github.com/Dugtai/microclimate.git
cd microclimate
```

## 2. Установка окружения

```bash
bash scripts/install.sh
```

После установки заполнить `.env`:

```bash
nano .env
```

В файл добавляются только локально:

```env
BOT_TOKEN=telegram_token_here
VK_TOKEN=vk_token_here
```

## 3. Проверка скриптов вручную

```bash
source .venv/bin/activate
python src/console_monitor.py
python src/data_logger.py
python src/telegram_bot_full.py
python src/vk_bot_full.py
```

## 4. Установка systemd-сервисов

Пример:

```bash
sudo cp systemd/microclimate-telegram-bot-full.service /etc/systemd/system/
sudo cp systemd/microclimate-vk-bot-full.service /etc/systemd/system/
sudo cp systemd/microclimate-data-logger.service /etc/systemd/system/
sudo cp systemd/microclimate-alert-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
```

Включение автозапуска:

```bash
sudo systemctl enable microclimate-telegram-bot-full.service
sudo systemctl enable microclimate-vk-bot-full.service
sudo systemctl enable microclimate-data-logger.service
sudo systemctl enable microclimate-alert-monitor.service
```

Запуск:

```bash
sudo systemctl start microclimate-telegram-bot-full.service
sudo systemctl start microclimate-vk-bot-full.service
sudo systemctl start microclimate-data-logger.service
sudo systemctl start microclimate-alert-monitor.service
```

## 5. Проверка состояния

```bash
systemctl status microclimate-telegram-bot-full.service --no-pager
systemctl status microclimate-vk-bot-full.service --no-pager
systemctl status microclimate-data-logger.service --no-pager
systemctl status microclimate-alert-monitor.service --no-pager
```

Логи:

```bash
journalctl -u microclimate-telegram-bot-full.service -n 100 --no-pager
journalctl -u microclimate-vk-bot-full.service -n 100 --no-pager
```

## 6. Wi‑Fi и автоподключение

Для настройки приоритетов сетей можно использовать шаблон:

```bash
bash scripts/wifi-priority-template.sh
```

Перед запуском заменить имена подключений или передать их через переменные окружения:

```bash
SCHOOL_WIFI="Интернет" HOME_WIFI="HomeWiFi" HOTSPOT_WIFI="MicroclimateAP" bash scripts/wifi-priority-template.sh
```

Логика:

- школьная сеть имеет самый высокий приоритет;
- домашняя сеть имеет меньший приоритет;
- собственная точка доступа стенда не поднимается автоматически;
- стенд ждёт появления известных сетей.

## 7. Диагностика

```bash
bash scripts/diagnostics.sh
```

Скрипт выводит:

- версию ядра;
- версию Python;
- сетевые интерфейсы;
- проверку сети;
- статусы сервисов;
- последние логи ботов.

## 8. Что не хранить в GitHub

В публичный репозиторий нельзя добавлять:

- реальные токены;
- пароли Wi‑Fi;
- внутренние IP-адреса;
- MAC-адреса;
- личные данные участников;
- скриншоты с приватными ID и QR-кодами без обработки.
