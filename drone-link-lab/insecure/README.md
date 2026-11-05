# Команди MAVLink і повтор повідомлень

У цій частині я дослідив передавання команд із Python до локального PX4 SITL. `replay.py` очікує HEARTBEAT на UDP 14540, надсилає COMMAND_LONG для ARM і TAKEOFF та виводить COMMAND_ACK.

```bash
python3 drone-link-lab/insecure/replay.py
```

У Wireshark використовується інтерфейс `lo` і фільтр `mavlink_proto && !icmp`. На скриншотах збережено поля команди TAKEOFF та відповідь ARM із результатом `MAV_RESULT_ACCEPTED`. Запис `mavlinc cap.pcapng` використовується для аналізу телеметрії.

## Відтворення повідомлень із запису

Для роботи з початковими байтами команд є `capture-and-replay.py`. Скрипт читає PCAP, знаходить ARM/TAKEOFF і показує номери кадрів. Так можна окремо вивчати повтор захопленого повідомлення та створення нової команди через pymavlink.

Порядок повторення досліду:

1. Запустити [локальний SITL](../sitl-setup.md), QGroundControl і захоплення на `lo`.
2. Передати ARM/TAKEOFF, зберегти команди, відповіді та телеметрію у `commands.pcapng`.
3. Переглянути список команд:

```bash
python3 drone-link-lab/insecure/capture-and-replay.py commands.pcapng
```

4. Вибрати номери кадрів зі свого запису. Приклад для кадрів 123 і 145:

```bash
python3 drone-link-lab/insecure/capture-and-replay.py commands.pcapng --frames 123 145 --send
```

Без `--send` працює режим перегляду. Під час передавання зберігаються MAVLink-байти, включно з sequence, timestamp і signature; IP/UDP-заголовки створюються для нового локального обміну. Скрипт використовує `127.0.0.1` і приймальні порти 14580/18570.

Результат команди перевіряється за COMMAND_ACK і станом симулятора у QGroundControl. Для досліду з підписаним повтором перше прийняття пакета та його повтор виконуються в одній сесії PX4, щоб зберегти стан перевірки часових міток.

[Підпис MAVLink 2](../secure/README.md).
