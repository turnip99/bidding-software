from django.db import models
from django.utils import timezone


class Item(models.Model):
    promiser = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    dt_live = models.DateTimeField('date/time up')
    dt_closed = models.DateTimeField('date/time down')
    base_price = models.FloatField(max_length=0)
    winning_name = models.CharField(max_length=50, blank=True, null=True)
    winning_price = models.FloatField(max_length=0, blank=True, null=True)

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


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    dt_bid = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    price = models.FloatField(max_length=0)

    def __str__(self):
        return str(self.item.name) + " - " + self.name + " - £" + str(self.price)
