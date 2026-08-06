def run_untrusted(code):
    # No sandbox
    # No resource limits
    # No monitoring
    exec(code, {"__builtins__": __builtins__})

# No WAF
# No RASP
# No container security