from histdb import insert_hist
from datetime import datetime, timezone

insert_hist(item_id="y1q9", amount=1, price=10000, date=datetime.now(tz=timezone.utc))
