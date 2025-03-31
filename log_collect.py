import os
from pathlib import Path

# Thư mục log trên Linux
log_dir = Path("/var/log/")

# Liệt kê tất cả file log
log_files = list(log_dir.glob("*.log"))

# Hiển thị danh sách file log
for log in log_files:
    print(log)

log_path = "/var/log/auth.log"  # Chỉnh theo file log bạn muốn kiểm tra

with open(log_path, "r", encoding="utf-8") as log_file:
    logs = log_file.readlines()

for line in logs[:10]:  # In ra 10 dòng đầu
    print(line.strip())

log_path = "/var/log/auth.log"

with open(log_path, "r", encoding="utf-8") as log_file:
    logs = log_file.readlines()

suspicious_logs = []

for line in logs:
    if "Failed password" in line or "authentication failure" in line:
        suspicious_logs.append(line.strip())

print("\n Các dòng log đáng ngờ:")
for log in suspicious_logs[:5]:  # In 5 dòng log đáng ngờ đầu tiên
    print(log)
