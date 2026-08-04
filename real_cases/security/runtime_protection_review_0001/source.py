def load_plugin(plugin_path):
    # No signature verification
    # No sandboxing
    with open(plugin_path, "rb") as f:
        code = f.read()
    exec(code)

def execute_task(task):
    # No resource limits
    # No timeout
    return eval(task["code"])