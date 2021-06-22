from django.db import models
from django.utils import timezone


class Item(models.Model):
    promiser = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    dt_live = models.DateTimeField('date/time up')
    dt_closed = models.DateTimeField('date/time down')
    base_price = models.FloatField(max_length=0)
    winning_name = models.CharField(max_length=50, blank=True, null=True)
    winning_phone_number = models.CharField(max_length=20, blank=True, null=True)
    winning_price = models.FloatField(max_length=0, blank=True, null=True)
    winners_num = models.IntegerField(default=1)

    def __str__(self):
        string = self.name
        if self.winning_price:
            string += " (" + self.winning_name + " - " + str(self.winning_price) + ")"
        return string

    @property
    def status(self):
        if self.closed:
            return "closed"
        elif self.live:
            return "live"
        else:
            return "upcoming"

    @property
    def live(self):
        now = timezone.now()
        return self.dt_live <= now and self.dt_closed > timezone.now()

    @property
    def closed(self):
        return self.dt_closed <= timezone.now()

    @property
    def formatted_winning_price(self):
        if self.winning_price:
            return '{:0,.2f}'.format(self.winning_price)
        else:
            return None

    @property
    def formatted_base_price(self):
        return '{:0,.2f}'.format(self.base_price)

    def bids(self):
        return Bid.objects.filter(item=self).order_by("-price")

    def additional_winners(self):
        additional_winners = []
        if self.winning_price and self.winners_num > 1:
            for bid in self.bids():
                if bid.name not in additional_winners and bid.name != bid.item.winning_name:
                    additional_winners.append(bid.name)
                if len(additional_winners) == self.winners_num-1:
                    break
        return additional_winners

    def time_until_close(self):
        diff = self.dt_closed - timezone.now()
        s = diff.seconds
        days = diff.days-1
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days > 1:
            string = str(days) + " days"
        elif days == 1:
            string = str(days) + " day"
        elif hours > 1:
            string = str(hours) + " hours"
        elif hours == 1:
            string = str(hours) + " hour"
        elif minutes > 1:
            string = str(minutes) + " minutes"
        elif minutes == 1:
            string = str(minutes) + " minute"
        elif seconds > 1:
            string = str(seconds) + " seconds"
        elif seconds == 1:
            string = str(seconds) + " second"
        else:
            string = ""
        return string


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    dt_bid = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    price = models.FloatField(max_length=0)

    def __str__(self):
        return str(self.item.name) + " - " + self.name + " - £" + str(self.price)
