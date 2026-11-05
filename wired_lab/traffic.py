import socket, ssl, subprocess, tempfile, threading

p = input("1 — HTTP; 2 — Telnet; 3 — FTP (тестові дані): ").strip()
t = input("TLS: 1 — так; 2 — ні: ").strip()
tls = t == "1"
payload = {
    "1": b"GET /?demo=WIFI_DEMO_12345 HTTP/1.1\r\nHost: localhost\r\n\r\n",
    "2": b"WIFI_DEMO_12345\r\n",
    "3": b"USER WIFI_DEMO_12345\r\nPASS DEMO_PASSWORD\r\n",
}[p]
port = 8443 if tls else {"1": 8080, "2": 2323, "3": 2121}[p]

# Приймач лише читає тестові дані; це не повні реалізації служб.
with tempfile.TemporaryDirectory() as d, socket.create_server(("127.0.0.1", port)) as server:
    server.settimeout(5)
    if tls:
        subprocess.run(
            [
                "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                "-keyout", d + "/key",
                "-out", d + "/cert",
                "-days", "1",
                "-subj", "/CN=localhost",
                "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1",
            ],
            check=True,
            capture_output=True,
        )
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(d + "/cert", d + "/key")

    def receive():
        raw, _ = server.accept()
        raw.settimeout(5)
        with (context.wrap_socket(raw, server_side=True) if tls else raw) as c:
            with c.makefile("rb") as stream:
                data = stream.read(len(payload))
            c.sendall(b"OK" if data == payload else b"NO")

    worker = threading.Thread(target=receive, daemon=True)
    worker.start()
    client = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    if tls:
        client.load_verify_locations(cafile=d + "/cert")
    client.keylog_filename = None
    with socket.create_connection(("127.0.0.1", port), timeout=5) as raw:
        with (client.wrap_socket(raw, server_hostname="localhost") if tls else raw) as c:
            c.sendall(payload)
            assert c.recv(2) == b"OK", "Дані не підтверджено"
            print(c.version() if tls else "Без TLS", "| Маркер: WIFI_DEMO_12345")
    worker.join(timeout=6)
