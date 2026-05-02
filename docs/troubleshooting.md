# Устранение неполадок

## Бот не отвечает

Проверить статус сервиса:

```bash
systemctl status microclimate-telegram-bot.service
```

Проверить последние логи:

```bash
journalctl -u microclimate-telegram-bot.service -n 100 --no-pager
```

## Ошибка с токеном

Если в логах указано, что токен не найден, необходимо проверить файл `.env`:

```bash
cat .env
```

В нём должны быть переменные:

```env
BOT_TOKEN=...
VK_TOKEN=...
```

## Нет подключения к сети

Проверить состояние сетевых интерфейсов:

```bash
ip a
```

Проверить доступность интернета:

```bash
ping -c 4 8.8.8.8
```

Проверить DNS:

```bash
ping -c 4 google.com
```

## Сервис не стартует после перезагрузки

Проверить, включён ли автозапуск:

```bash
systemctl is-enabled microclimate-telegram-bot.service
```

Если сервис выключен:

```bash
sudo systemctl enable microclimate-telegram-bot.service
```

## Бот запускается раньше сети

В service-файле должны быть строки:

```ini
After=network-online.target
Wants=network-online.target
```

После изменения service-файла выполнить:

```bash
sudo systemctl daemon-reload
sudo systemctl restart microclimate-telegram-bot.service
```

## Telegram API недоступен

Если Telegram недоступен из текущей сети, можно использовать резервный канал через VK API. Именно поэтому в проект была добавлена параллельная интеграция с VK.
