# Каталог `scripts`

В этом каталоге находятся вспомогательные shell-скрипты для установки, диагностики, настройки Wi‑Fi и реакции на появление сети.

## Файлы

| Файл | Назначение |
|---|---|
| `install.sh` | установка проекта на стенд: виртуальное окружение, зависимости, `.env`, каталоги `data/` и `logs/` |
| `install-project.sh` | альтернативный установочный скрипт для подготовки проекта |
| `diagnostics.sh` | диагностика Linux-стенда, сети, Python, systemd-сервисов и логов |
| `wifi-connect.sh` | подключение к Wi‑Fi через `nmcli` |
| `wifi-priority-template.sh` | шаблон настройки приоритетов Wi‑Fi-сетей |
| `restart-bots-on-network.sh` | ожидание сети и перезапуск сервисов ботов после подключения |
| `NetworkManager-dispatcher-template.sh` | шаблон NetworkManager dispatcher для реакции на события сети |

## Быстрая установка

```bash
bash scripts/install.sh
```

## Диагностика

```bash
bash scripts/diagnostics.sh
```

## Настройка Wi‑Fi

Пример подключения:

```bash
sudo WIFI_SSID="network_name" WIFI_PASSWORD="password" bash scripts/wifi-connect.sh
```

Пример настройки приоритетов:

```bash
SCHOOL_WIFI="Интернет" HOME_WIFI="HomeWiFi" HOTSPOT_WIFI="MicroclimateAP" bash scripts/wifi-priority-template.sh
```

## Безопасность

В публичные скрипты не добавляются реальные SSID, пароли, токены, IP-адреса и MAC-адреса. Все чувствительные значения передаются через переменные окружения или локальный `.env`, который не публикуется в GitHub.
