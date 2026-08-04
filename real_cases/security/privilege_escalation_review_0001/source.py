def setuid_program():
    os.setuid(0)
    os.system("whoami")

def run_as_sudo():
    os.system("sudo whoami")

# Hardcoded sudo password
SUDO_PASSWORD = "sudo123"