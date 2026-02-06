import json
from datetime import datetime

def log_action(action, details):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    }

    with open("audit/audit_log.json", "a") as f:
        f.write(json.dumps(entry) + "\n")
