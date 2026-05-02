# Обзор скриптов проекта

В репозитории собраны основные программные компоненты стенда мониторинга микроклимата.

## Основная логика

| Файл | Назначение |
|---|---|
| `src/microclimate_core.py` | чтение параметров, анализ, форматирование сообщений |
| `src/thresholds.py` | пороговые значения и рекомендации |
| `src/sensors_live.py` | базовая демонстрационная версия чтения датчиков |

## Боты

| Файл | Назначение |
|---|---|
| `src/telegram_bot.py` | базовый Telegram-бот |
| `src/vk_bot.py` | базовый VK-бот |
| `src/telegram_bot_full.py` | расширенный Telegram-бот со всеми командами |
| `src/vk_bot_full.py` | расширенный VK-бот со всеми командами |

## Мониторинг и сбор данных

| Файл | Назначение |
|---|---|
| `src/console_monitor.py` | вывод текущих параметров в консоль |
| `src/display_monitor.py` | заготовка для вывода параметров на LCD/экран |
| `src/data_logger.py` | запись измерений в CSV |
| `src/alert_monitor.py` | контроль отклонений с подтверждением нескольких измерений |

## Системные скрипты

| Файл | Назначение |
|---|---|
| `scripts/install.sh` | установка зависимостей и подготовка окружения |
| `scripts/diagnostics.sh` | диагностика Linux-стенда и сервисов |
| `scripts/wifi-connect.sh` | подключение к Wi-Fi через NetworkManager/nmcli |
| `scripts/restart-bots-on-network.sh` | перезапуск ботов после появления сети |

## systemd-сервисы

| Файл | Назначение |
|---|---|
| `systemd/microclimate-telegram-bot.service` | базовый Telegram-бот |
| `systemd/microclimate-vk-bot.service` | базовый VK-бот |
| `systemd/microclimate-telegram-bot-full.service` | расширенный Telegram-бот |
| `systemd/microclimate-vk-bot-full.service` | расширенный VK-бот |
| `systemd/microclimate-console-monitor.service` | консольный монитор |
| `systemd/microclimate-display-monitor.service` | монитор для дисплея |
| `systemd/microclimate-data-logger.service` | CSV-логгер |
| `systemd/microclimate-alert-monitor.service` | монитор отклонений |

## Что не публикуется

В репозиторий намеренно не добавляются:

- реальные токены Telegram и VK;
- пароли Wi-Fi;
- реальные SSID школьных сетей;
- персональные идентификаторы пользователей;
- чувствительные сетевые параметры;
- скрипты, способные нарушить удалённый доступ к устройству при неправильной настройке.

## Как использовать на стенде

1. Склонировать репозиторий.
2. Запустить `scripts/install.sh`.
3. Создать `.env` на основе `.env.example`.
4. Заполнить токены.
5. Установить нужные service-файлы из каталога `systemd/`.
6. Включить автозапуск через `systemctl enable`.
7. Проверить работу через `scripts/diagnostics.sh` и `journalctl`.
