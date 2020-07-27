from datetime import datetime, timedelta
print((datetime.now().date() - timedelta(days=2)).strftime("%d.%m.%Y")[:8])