from datetime import datetime
import shutil

def backup_database(path="marcus_memory.db"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}_{timestamp}.bak"
    shutil.copyfile(path, backup_path)
    print(f"✅ Backup created: {backup_path}")
