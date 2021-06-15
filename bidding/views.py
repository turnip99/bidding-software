import locale

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect

from .models import Item, Bid


def name_input(request):
  if request.method == 'GET':
    return render(request, 'name_input.html', {})
  else:
    return HttpResponseRedirect("/bidding/?name=" + request.POST["name"])


def index(request):
  items = Item.objects.all().order_by("-dt_closed")
  items_upcoming = []
  items_live = []
  items_closed = []
  for item in items:
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
  return render(request, 'index.html', context)


def update_bids(request):
  items = Item.objects.all()
  item_updates = {}
  for item in items:
    if item.status != "upcoming":
      item_updates[item.id] = {"status": item.status, "winning_price": item.formatted_winning_price, "winning_name": item.winning_name}
      if item.status == "live":
        item_updates[item.id]["dt_closed"] = item.dt_closed.strftime("%d-%m-%Y %H:%M")
  return JsonResponse({'item_updates': item_updates})


def add_bid(request, item_id, price, name):
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
  if item.winning_price and price <= item.winning_price:
    error = "You bid must be higher than the current winning bid (£" + item.formatted_winning_price + ")."
  else:
    Bid.objects.create(item=item, name=name, price=price)
    item.winning_price = price
    item.winning_name = name
    item.save()
  return JsonResponse({'error': error})
