from datetime import timedelta
from random import randint
from django.utils import timezone
from bidding.models import Item, Bid

now = timezone.now()
minus_one_hundred_years = now - timedelta(days=200)
minus_two_hundred_days = now - timedelta(days=100)
one_hundred_days = now + timedelta(days=100)
for i in range(1, 70):
    winners_num = randint(1, 5)
    base_price = randint(1, 10)
    winning_price = randint(base_price, 25)
    if randint(1, 2) == 1:
        dt_live = now
        dt_closed = one_hundred_days
    else:
        dt_live = minus_two_hundred_days
        dt_closed = minus_one_hundred_years
    item = Item.objects.create(promiser="Stress Test", name=f"Promise {i}", dt_live=dt_live, dt_closed=dt_closed, base_price=base_price, winners_num=winners_num, winning_name="Captain Winner", winning_phone_number="07000000000", winning_price=winning_price)
    Bid.objects.create(item=item, dt_bid=now, name="Captain Winner", phone_number="07000000000", price=winning_price)
    for j in range(base_price, winning_price):
        Bid.objects.create(item=item, dt_bid=now, name=f"Captain Loser £{j}", phone_number=f"070000000{j}", price=j)
