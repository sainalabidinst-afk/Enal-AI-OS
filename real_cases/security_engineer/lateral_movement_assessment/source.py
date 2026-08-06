import paramiko

def ssh_connect(host, username, password):
    # No bastion host
    # No network segmentation
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    return ssh

def pivot_through_server(server):
    # No network segmentation
    ssh = ssh_connect(server, "admin", "password")
    if ssh:
        stdin, stdout, stderr = ssh.exec_command("curl http://internal-db:5432")
        return stdout.read()
    return None