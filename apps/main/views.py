from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import Items
from ..login.models import User
from django.contrib import messages

from django.core.urlresolvers import reverse
from django.db.models import Count
import datetime


# Create your views here.
#Views needed
# 1. render index.html - DONE
# 2. show items on index.html
# 3. render add items.html -
# 4. add items to wishlist models
# 5. render details.html -
# 6. show individuals who have the item on thier lists
# 7. allow user to add items to thier lists... Many-to-Many challege?

def index(request): # 1. render index.html
    if "id" not in request.session:
        return redirect("login:index")
    else:
        context = {
        'user_items':Items.objects.filter(user_id=request.session["id"]),
        "user": User.objects.get(id=request.session["id"]),
        'other_user_items':Items.objects.exclude(user_id=request.session["id"]),
        }
    return render(request, "main/index.html", context)

def items(request):
    if "id" not in request.session:
        return redirect("login:index")

    return render(request, "main/items.html")

def add(request):
    if "id" not in request.session:
        return redirect("login:index")

    item_info = {}
    if request.method == "POST":
        item_info = {
        'item': request.POST['item'],
        'user_id': request.session['id'],
        }
    result = Items.objects.add_item(item_info)
    if result['errors'] == None:
        return redirect("main:index")
    else:
        for error in result['errors']:
            messages.error(request, error)
        return redirect("items/add")

def join_item(request, id):
    add_data = {
    'item_id': id,
    'user_id': request.session['id']
    }
    Items.objects.add_user(add_data)
    return redirect('main:index')

def remove_item(request, id):
    remove_data = {
    'item_id': id,
    'user_id': request.session['id']
    }
    Items.objects.remove_user(remove_data)
    return redirect('main:index')

def delete_item(request, id):
    delete = {
    'item_id': id,
    }
    Items.objects.delete_data(delete)
    return redirect('main:index')

def details(request, id):
    if "id" not in request.session:
        return redirect("login:index")
    context = {'item':Items.objects.get(id=id)}
    return render(request, "main/details.html", context)
