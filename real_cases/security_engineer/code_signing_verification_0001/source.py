def install_plugin(plugin_path):
    # No signature verification
    # No sandboxing
    with open(plugin_path, "rb") as f:
        code = f.read()
    exec(code)

BUILD_ARTIFACT = None  # Not signed