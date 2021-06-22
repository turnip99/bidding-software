import locale

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect

from .models import Item, Bid


def name_input(request):
  if request.method == 'GET':
    return render(request, 'name_input.html', {})
  else:
    return HttpResponseRedirect("/bidding/?name=" + request.POST["name"] + "&phone_number=" + request.POST["phone_number"])


def bidding(request):
  items = Item.objects.all().order_by("-dt_closed")
  items_upcoming = []
  items_live = []
  items_closed = []
  for item in items:
    item.additional_winners = item.additional_winners()
    if item.live:
      items_live.append(item)
    elif item.closed:
      items_closed.append(item)
    else:
      items_upcoming.append(item)

  context = {
    'items_upcoming': items_upcoming,
    'items_live': items_live,
    'items_closed': items_closed,
  }
  return render(request, 'bidding.html', context)


def update_bids(request):
  items = Item.objects.all()
  item_updates = {}
  for item in items:
    if item.status != "upcoming":
      item_updates[item.id] = {"status": item.status, "winning_price": item.formatted_winning_price, "winning_name": item.winning_name, "additional_winners": item.additional_winners()}
      if item.status == "live":
        item_updates[item.id]["dt_closed"] = item.dt_closed.strftime("%d-%m-%Y %H:%M")
        item_updates[item.id]["remaining"] = item.time_until_close()
  return JsonResponse({'item_updates': item_updates})


def add_bid(request, item_id, price, name, phone_number):
  item = get_object_or_404(Item, id=item_id)
  error = ""
  try:
    price = float(price)
  except:
    return JsonResponse({"error": "Your bid must be a number! What are you playing at? O.o"})
  if item.status != "live":
    if item.status == "unopened":
      error = "This item has not yet gone live. How did you even get here? :/"
    else:
      error = "This item is no longer live. Sorry about that. :("
  elif item.winning_price:
    if item.winners_num == 1:
      if item.winning_name == name and item.winning_phone_number == phone_number:
        error = "You're already winning this item - no need to outbid yourself!"
      elif price <= item.winning_price:
        error = "Your bid must be higher than the current winning bid (£" + item.formatted_winning_price + ")."
    elif item.winners_num > 1:
      lowest_winning_price = item.lowest_winning_price()
      highest_user_price = item.highest_user_price(name, phone_number)
      if price <= lowest_winning_price:
        error = "Your bid must be higher than the current lowest winning bid (£" + '{:0,.2f}'.format(lowest_winning_price) + ")."
      elif price <= highest_user_price:
        error = "Your bid must be higher than your previous bid (£" + '{:0,.2f}'.format(highest_user_price) + ")."
  elif price < item.base_price:
    error = "You bid must be higher than base price (£" + item.formatted_base_price + ")."
  if error == "":
    Bid.objects.create(item=item, name=name, price=price, phone_number=phone_number)
    if price > item.winning_price:
      item.winning_price = price
      item.winning_name = name
      item.winning_phone_number = phone_number
      item.save()
  return JsonResponse({'error': error})

