# Декодер MAVLink для Wireshark

`mavlink_common.lua` - згенерований Lua-декодер діалекту common, який використовується на цьому стенді. Він дозволяє переглядати типи повідомлень, системні ідентифікатори, поля телеметрії та команд.

Встановлення з кореня проєкту:

```bash
install -Dm644 tools/wireshark/mavlink_common.lua "$HOME/.local/lib/wireshark/plugins/mavlink_common.lua"
```

Після цього перезапустити Wireshark. Фільтр: `mavlink_proto && !icmp`.

[Офіційний спосіб генерації через pymavlink/mavgen](https://mavlink.io/en/guide/wireshark.html). Якщо плагін уже є, не встановлювати другу копію з іншим ім'ям у той самий каталог.
