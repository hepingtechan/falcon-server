import sys
sys.path.append('.')
from server.usermonitor.sensitive_command import rm

# 3004
def turnOnSensitiveCommandManagement(data):
    rm.modify_rm_implement()
    return "ok!-open"

# 3005
def turnOffSensitiveCommandManagement(data):
    rm.recovery_rm_implement()
    return "ok!-close"

if __name__ == '__main__':
    a="ok"
    turnOnSensitiveCommandManagement(a)
    # turnOffSensitiveCommandManagement(a)
