from __future__ import unicode_literals
from django.db import models
from ..login.models import User
from django.db.models import Count
import datetime


class ItemManager(models.Manager):
    def add_item(self, postData):
        print postData
        errors = []
        if len(postData["item"]) < 1:
            errors.append("Item field cannot be blank.")

        if len(errors) == 0:
            user = User.objects.get(id=postData['user_id'])
            print user.name
            item = Items.objects.create(item=postData['item'], created_by = user)
            item.user_id.add(user)
            print item
            return {'errors': None}
        else:
            return {'errors': errors}

    def add_user(self, postData):
        item = Items.objects.get(id = postData['item_id'])
        user = User.objects.get(id=postData['user_id'])
        item.user_id.add(user)
        return
    def remove_user(self, postData):
        item = Items.objects.get(id = postData['item_id'])
        user = User.objects.get(id=postData['user_id'])
        item.user_id.remove(user)
        return
    def delete_data(self, postData):
        Items.objects.get(id = postData['item_id']).delete()
        return

class Items(models.Model):
    user_id = models.ManyToManyField(User, related_name='joined')
    created_by = models.ForeignKey(User, related_name='creator')
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
