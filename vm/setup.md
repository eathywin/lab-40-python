# Стенд і початок роботи

Роботу виконано на повноцінному Kali Linux. Для різних дослідів використано локальний мережевий обмін, власну Wi-Fi-мережу та симулятор польоту.

## Обладнання та програми

- Kali Linux, Python 3, OpenSSL, Wireshark/tshark, Aircrack-ng і Docker.
- USB-адаптер Mercusys, USB ID `2c4e:0102`, драйвер `rtl8xxxu`, інтерфейс `wlan0`.
- Власний роутер TP-Link TL-WR850N v2, WPA2-Personal із AES/CCMP.
- PX4 SITL SIH і QGroundControl для роботи з MAVLink.

Базові пакети Kali:

```bash
sudo apt install python3 openssl wireshark tshark aircrack-ng python3-pymavlink make
```

Для створення PDF локально використовуються `python3-reportlab` і `fonts-dejavu-core`; для перегляду сторінок - `poppler-utils`.

## Порядок виконання

1. Відкрити Wireshark на `lo` і виконати [TCP/TLS-дослід](../wired_lab/setup.md).
2. Перейти до [Wi-Fi-частини](../wifi_lab/setup.md). Під час monitor mode адаптер використовується для захоплення кадрів; для звичайного доступу до мережі зручно під'єднати Ethernet.
3. Запустити [PX4 SIH і QGroundControl](../drone-link-lab/sitl-setup.md), почати захоплення MAVLink на `lo`.
4. Переглянути результати у [звіті](../defender-report.pdf).

Якщо в локальній копії є допоміжні `scripts/`, `make check` перевіряє файли, посилання та синтаксис, а `make report` формує PDF. Самостійний запуск основної демонстрації: `python3 wired_lab/traffic.py`.
