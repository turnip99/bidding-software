from tokenize import String
from django.db import models
from django.utils import timezone


class AuctionSetting(models.Model):
    active = models.BooleanField(default=False)
    auction_name = models.CharField(max_length=500, default="Promise Auction Bidding System")
    is_promise_auction = models.BooleanField(default=True, verbose_name="Is this a promise auction (as opposed to a conventional auction)?")
    primary_colour = models.CharField(max_length=7, default="#000080", help_text="Hex code. Used for some text on the website.")
    max_bid = models.DecimalField(decimal_places=2, max_digits=12, default=999.99, help_text="The highest bid someone can make on this auction.")
    bid_sync_regularity = models.IntegerField(default=10, help_text="How often the winning bids on the bidding page are synced with the server (in seconds).")
    enable_leaderboard = models.BooleanField(default=True)
    leaderboard_spaces = models.IntegerField(default=10, blank=True, null=True, help_text="The top X bidders to appear on the leaderboard. Leave blank to display all bidders on the leaderboard.")
    payment_account_holder_name = models.CharField(max_length=100, blank=True, null=True, help_text="Used in the message generator.")
    payment_account_number = models.CharField(max_length=8, blank=True, null=True, help_text="Used in the message generator.")
    payment_sort_code = models.CharField(max_length=8, blank=True, null=True, help_text="Used in the message generator.")
    payment_reference = models.CharField(max_length=20, blank=True, null=True, default="*your name*", help_text="Used in the message generator.")

    class Meta:
        ordering = ("id",)

    def __str__(self):
        string = f"{self.auction_name}"
        if self.active:
            string += " (ACTIVE)"
        else:
            string += " (INACTIVE)"
        return string


class AuctionDescriptionBulletPoint(models.Model):
    text = models.CharField(max_length=500, default="After the auction, you will be contacted with any promises that you have won.", help_text="The bullet points are displayed at the top of the bidding page. You may want to mention where the money raised will go going, the process to redeeming items, etc.")
    auction = models.ForeignKey(AuctionSetting, on_delete=models.CASCADE)
    loc = models.IntegerField(default=0, help_text="Denotes the order that the bullet point appear compared to others.")

    class Meta:
        ordering = ("loc", "id")

    def __str__(self):
        return f"{self.auction.auction_name} - {self.text}"


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

    class Meta:
        ordering = ("id",)

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
        return self.dt_live <= now and self.dt_closed > now

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

    def additional_winners(self):
        additional_winners = []
        winning_names_numbers = []
        if self.winning_price and self.winners_num > 1:
            for bid in self.bid_set.all():
                if not in_winning_names_numbers(winning_names_numbers, bid) and (bid.name != bid.item.winning_name or bid.phone_number != bid.item.winning_phone_number):
                    additional_winners.append({"position": number_to_position(len(additional_winners)+2), "name": bid.name, "phone_number": bid.phone_number, "price": bid.formatted_price, "price_raw": bid.price})
                    winning_names_numbers.append({"name": bid.name, "phone_number": bid.phone_number})
                if len(additional_winners) == self.winners_num-1:
                    break
        return additional_winners

    def lowest_winning_price(self):
        additional_winners = self.additional_winners()
        if additional_winners:
            return float(additional_winners[-1]["price"])
        else:
            return self.winning_price

    def highest_user_price(self, name, phone_number):
        highest_user_bid = Bid.objects.filter(item=self, name=name, phone_number=phone_number).order_by("-price").first()
        if highest_user_bid:
            return float(highest_user_bid.price)
        else:
            return 0

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

    class Meta:
        ordering = ("-price",)

    def __str__(self):
        return str(self.item.name) + " - " + self.name + " - £" + str(self.price)

    @property
    def formatted_price(self):
        return '{:0,.2f}'.format(self.price)


def number_to_position(num):
  if num == 1:
    return "1st"
  elif num == 2:
    return "2nd"
  elif num == 3:
    return "3rd"
  else:
    return str(num) + "th"


def in_winning_names_numbers(winning_names_numbers, bid):
    for winning_name_number in winning_names_numbers:
        if winning_name_number["name"] == bid.name and winning_name_number["phone_number"] == bid.phone_number:
            return True
    return False
