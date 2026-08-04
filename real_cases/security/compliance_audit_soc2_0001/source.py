def audit_log(event):
    # No SOC2 compliance
    # No integrity check
    logger.info(event)

def access_control(user, resource):
    # No least privilege
    return True

def data_backup():
    # No encryption
    copy("/data", "/backup")
    return True