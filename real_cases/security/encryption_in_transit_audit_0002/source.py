def send_sensitive(data):
    # No encryption in transit
    # Hardcoded key
    ENCRYPTION_KEY = "encryption_key_12345"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("internal", 8080))
    sock.sendall(data.encode())