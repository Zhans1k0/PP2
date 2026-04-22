from datetime import datetime, timedelta

now = datetime.now()
print(now)

formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)

date1 = datetime(2024, 1, 1)
date2 = datetime(2024, 12, 31)

diff = date2 - date1
print(diff.days)

future = now + timedelta(days=10)
print(future)

past = now - timedelta(hours=5)
print(past)