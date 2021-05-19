from django.contrib import admin

# Register your models here.
from .models import User,Category,AuctionList,Bid,Comments

admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionList)
admin.site.register(Bid)
admin.site.register(Comments)
