from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    

class Category(models.Model):
    category = models.CharField(max_length = 30)
    def __str__(self):
        return f"{self.category}"

class AuctionList(models.Model):
    # Data contained with the data base
    name = models.CharField(max_length = 30)
    description = models.TextField(blank = True, null = True)
    initial_bid = models.DecimalField(decimal_places= 2,null= False,blank= False,max_digits = 1000)
    status = models.BooleanField(default = True) 
    date_created = models.DateTimeField(default = timezone.now)
    image_link1 = models.CharField(max_length=100, blank = True, null = True)
    image_link2 = models.CharField(max_length=100, blank = True, null = True)
    image_link3 = models.CharField(max_length=100, blank = True, null = True)
    image_link4 = models.CharField(max_length=100, blank = True, null = True)
    image_link5 = models.CharField(max_length=100, blank = True, null = True)
    current_largest_bid = models.DecimalField(decimal_places = 2,null = True,blank = True,max_digits = 1000) 
    # Related data

    owner_id = models.ForeignKey(User, on_delete = models.PROTECT ,related_name = "all_creator_listing")
    watchers = models.ManyToManyField(User, blank=True ,related_name = 'watched_lists')
    # comments = models.ForeignKey(Comments, on_delete = models.CASCADE, related_name= "comments_associated")
    # current_bid = models.ForeignKey(Bid,on_delete= CASCADE , related_name = "bids")
    category = models.ForeignKey(Category, on_delete= models.CASCADE,related_name= "categories")
    winner = models.ForeignKey(User, null = True,blank=True , on_delete=models.PROTECT)
    # picture = models.ForeignKey(Pictures, on_delete= models.PROTECT, )

    # FOR DISPLAY PURPOSES
    def __str__(self):
        return f"{self.name}"



class Bid(models.Model):
    auction_id = models.ForeignKey(AuctionList,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places = 2, max_digits=1000 ,null= False)
    date = models.DateTimeField(default = timezone.now)

    # FOR DISPLAY PURPOSES
    def __str__(self):
        return f"{self.user}-{self.amount}"

class Comments(models.Model):
    comment = models.CharField(max_length= 300)
    date = models.DateTimeField(default = timezone.now) 
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    auction_id = models.ForeignKey(AuctionList, on_delete= models.CASCADE , related_name = "comments")

    # FOR DISPLAY PURPOSES
    def __str__(self):
        return f"{self.user}-{self.comment}"


