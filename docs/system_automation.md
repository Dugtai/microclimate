# Системная автоматизация стенда

В проекте использовалась системная автоматизация на Linux, чтобы стенд мог работать автономно после включения питания.

## Что автоматизируется

- подключение к известной Wi-Fi-сети;
- запуск Telegram-бота;
- запуск VK-бота;
- локальный вывод показаний на экран или консоль;
- перезапуск сервисов при сбоях;
- восстановление после перезагрузки устройства.

## systemd-сервисы

В каталоге `systemd/` находятся service-файлы:

```text
microclimate-telegram-bot.service
microclimate-vk-bot.service
microclimate-telegram-bot-full.service
microclimate-vk-bot-full.service
microclimate-console-monitor.service
```

Расширенные версии используют файлы:

```text
src/telegram_bot_full.py
src/vk_bot_full.py
src/console_monitor.py
```

## Установка сервиса

Пример для расширенного Telegram-бота:

```bash
sudo cp systemd/microclimate-telegram-bot-full.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable microclimate-telegram-bot-full.service
sudo systemctl start microclimate-telegram-bot-full.service
```

Проверка:

```bash
systemctl status microclimate-telegram-bot-full.service
journalctl -u microclimate-telegram-bot-full.service -n 100 --no-pager
```

## Подключение к Wi-Fi

В каталоге `scripts/` добавлен пример скрипта `wifi-connect.sh`, который использует `nmcli` и переменные окружения:

```bash
sudo WIFI_SSID="имя_сети" WIFI_PASSWORD="пароль" ./scripts/wifi-connect.sh
```

Для открытой сети пароль можно не указывать.

## Перезапуск сервисов после появления сети

Скрипт `scripts/restart-bots-on-network.sh` ожидает доступность сети и перезапускает сервисы проекта. Его можно использовать вручную или как основу для NetworkManager dispatcher.

## Watchdog

В реальном стенде использовался watchdog для контроля доступности сети и перезапуска сервисов. В публичный репозиторий не добавляется вариант с жёстким перезапуском сетевого стека, чтобы не публиковать потенциально опасный для удалённого доступа скрипт.

Безопасный подход для публичной версии:

- использовать `Restart=always` в systemd-сервисах;
- указывать `RestartSec=10`;
- запускать сервисы после `network-online.target`;
- проверять состояние через `journalctl`;
- не хранить реальные SSID, пароли и токены в репозитории.
