# Захист мережевих і MAVLink-каналів

У цій роботі я порівняв відкритий TCP-обмін із TLS, дослідив WPA2-рукостискання власної Wi-Fi-мережі та проаналізував MAVLink у PX4 SITL. Для кожної частини зберіг записи трафіку й скриншоти, щоб показати результат у Wireshark.

Стенд: Kali Linux, Wireshark, Python, USB-адаптер Mercusys, роутер TP-Link TL-WR850N v2, Docker, PX4 SITL SIH і QGroundControl. TCP/TLS та MAVLink досліджувалися локально через `lo`, а Wi-Fi - через адаптер у monitor mode.

## Результати роботи

| Частина | Результат |
|---|---|
| TCP і TLS | Порівняно відкритий тестовий маркер із зашифрованим обміном TLS 1.3 |
| Сертифікати | Перевірено довіру до сертифіката та відповідність імені сервера |
| Wi-Fi | Захоплено чотири повідомлення WPA2-рукостискання та проведено контрольну словникову перевірку |
| MAVLink | Розібрано телеметрію, команди ARM/TAKEOFF і відповідь на ARM |
| Підпис MAVLink 2 | Налаштовано signing у QGroundControl; зафіксовано статус Signing OK і результат запуску тестового клієнта |
| Захист Wi-Fi | Порівняно WPA2-Personal, WPA2-Enterprise і WPA3; розглянуто KRACK та Dragonblood |

## Звіт та інструкції

- [Звіт у PDF](defender-report.pdf) і [текст звіту](defender-report.md).
- [Стенд і початок роботи](vm/setup.md).
- [TCP/TLS: запуск](wired_lab/setup.md) та [результати](wired_lab/notes.md).
- [Wi-Fi: захоплення](wifi_lab/setup.md) та [порівняння захисту](wifi_lab/notes.md).
- [Запуск PX4 SITL](drone-link-lab/sitl-setup.md), [команди MAVLink](drone-link-lab/insecure/README.md) та [підпис повідомлень](drone-link-lab/secure/README.md).
- [Лабораторне середовище](ETHICS.md).

## Швидкий запуск

Команди виконуються з кореня проєкту:

```bash
python3 wired_lab/traffic.py
```

У меню цифрою вибирається тип тестових даних, потім - використання TLS. Перед запуском у Wireshark потрібно почати захоплення на `lo`.

```text
tcp.port == 8080 || tcp.port == 2323 || tcp.port == 2121 || tcp.port == 8443
```

Для MAVLink використовується фільтр `mavlink_proto && !icmp` після встановлення [Lua-декодера](tools/wireshark/README.md). Для WPA2-рукостискання - `eapol`.

## Структура проєкту

`wired_lab/` містить TCP/TLS-демонстрацію, `wifi_lab/` - дослідження власної бездротової мережі, `drone-link-lab/` - обмін із симулятором. У кожній частині є інструкції та матеріали досліду. Підсумки зібрані у звіті.
