# PX4 SITL і QGroundControl

Я використовую SIH для квадрокоптера: фізика й автопілот працюють у симуляторі, окреме вікно Gazebo не потрібне. У QGroundControl видно стан і телеметрію. MAVLink запускається разом із PX4.

Якщо вихідний код уже є у ~/PX4-Autopilot, команду попереднього стенда можна повторити:

```bash
cd ~/PX4-Autopilot
sudo docker run --rm -it --network host   --user "$(id -u):$(id -g)" -e CCACHE_DIR=/tmp/ccache   -v "$PWD":/px4 -w /px4   px4io/px4-dev:v1.17.0-beta1 make px4_sitl_sih sihsim_quadx
```

Цей тег визначає середовище збірки, а не версію коду PX4. Для нового запуску треба записати `git rev-parse HEAD` у каталозі PX4 і `ver all` у консолі `pxh>`. Зберегти також версію QGC з About.

Після `pxh>` відкрити QGroundControl. Для одного екземпляра типова схема така:

| Зв'язок | Куди PX4 надсилає | Де PX4 приймає |
|---|---:|---:|
| QGroundControl | 14550 | 18570 |
| Python/API | 14540 | 14580 |

Wireshark: `lo`, фільтр `udp.port == 14550 || udp.port == 18570 || udp.port == 14540 || udp.port == 14580`.

Для декодування MAVLink додано копію наявного Lua-декодера в `tools/wireshark/`. Встановлення - `make install-dissector`, після чого перезапустити Wireshark. Фільтр цього декодера: `mavlink_proto && !icmp`.

ICMP Port unreachable на інших потоках означає, що UDP-порт не має слухача. Це не є підтвердженням збою всіх MAVLink-зв'язків. Перед дослідом ARM/TAKEOFF симулятор має бути готовий до польоту. Preflight-відмова і відхилення за підписом - різні результати.

[Офіційна інструкція PX4 SIH](https://docs.px4.io/main/en/sim_sih/).
