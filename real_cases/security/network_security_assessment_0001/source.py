def send_unencrypted(data):
    sock = connect_insecure("example.com", 80)
    sock.sendall(data.encode())

def insecure_ssh():
    # No host key verification
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("host", username="user", password="pass")