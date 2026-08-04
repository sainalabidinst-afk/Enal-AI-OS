import os
import subprocess

def run_as_root():
    os.system("sudo apt-get update")

def execute_shell(command):
    result = subprocess.call(command, shell=True)

def admin_panel(request):
    if request.user.is_admin:
        os.system("rm -rf /tmp/*")
        return "Admin actions completed"

@app.route("/sudo")
def sudo_command():
    cmd = request.args.get("cmd")
    return subprocess.check_output(cmd, shell=True)

# Hardcoded admin password
ADMIN_PASSWORD = "admin123"