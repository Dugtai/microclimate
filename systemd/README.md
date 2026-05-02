# Каталог `systemd`

В этом каталоге находятся service-файлы для автозапуска компонентов проекта на Linux-стенде.

## Назначение

`systemd` используется для того, чтобы после включения питания стенд автоматически запускал нужные части системы и восстанавливал их работу при сбоях.

## Файлы

| Файл | Назначение |
|---|---|
| `microclimate-telegram-bot.service` | базовый Telegram-бот |
| `microclimate-vk-bot.service` | базовый VK-бот |
| `microclimate-telegram-bot-full.service` | расширенный Telegram-бот |
| `microclimate-vk-bot-full.service` | расширенный VK-бот |
| `microclimate-console-monitor.service` | консольный монитор показаний |
| `microclimate-display-monitor.service` | монитор для дисплея/LCD |
| `microclimate-data-logger.service` | запись истории измерений в CSV |
| `microclimate-alert-monitor.service` | контроль отклонений параметров |

## Установка сервиса

Пример для расширенного Telegram-бота:

```bash
sudo cp systemd/microclimate-telegram-bot-full.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable microclimate-telegram-bot-full.service
sudo systemctl start microclimate-telegram-bot-full.service
```

## Проверка

```bash
systemctl status microclimate-telegram-bot-full.service --no-pager
journalctl -u microclimate-telegram-bot-full.service -n 100 --no-pager
```

## Важное замечание

В service-файлах используются пути вида:

```text
/home/root/microclimate
```

Если проект установлен в другой каталог, пути в service-файлах нужно изменить под реальное расположение проекта.
