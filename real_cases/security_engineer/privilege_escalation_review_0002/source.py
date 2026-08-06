def escalate_privileges():
    # No privilege check
    # No authorization
    os.system("su -")
    os.system("whoami")

# Hardcoded root password
ROOT_PASSWORD = "root123"