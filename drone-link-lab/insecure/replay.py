from pymavlink import mavutil

m = mavutil.mavlink_connection("udpin:127.0.0.1:14540")
m.wait_heartbeat()
print("SITL відповів")

for cmd, p1, p7 in [(400, 1, 0), (22, 0, 5)]:
    m.mav.command_long_send(
        m.target_system, m.target_component, cmd, 0,
        p1, 0, 0, 0, 0, 0, p7
    )
    print(m.recv_match(type="COMMAND_ACK", blocking=True, timeout=5))
