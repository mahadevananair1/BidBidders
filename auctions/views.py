from typing import Dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import AuctionForm, AuctionWatchers, Bidform, CommentForm
from .models import  Bid, Category, Comments, User,AuctionList
import operator

def index(request):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""   

    """ didint complete aution info view etc """
     # list of products available
    products = AuctionList.objects.filter(status = True)
    print(products)
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    
    return render(request, "auctions/index.html",{
        'watcher_count' : obj_count,
        'products':products,
        'empty': empty
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def activelisting(request):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""

    """ didint complete aution info view etc """
     # list of products available
    products = AuctionList.objects.filter(status = True)
    print(products)
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/activelisting.html", {
        "products": products,
        "empty": empty,
        "watcher_count": obj_count
    })

def closedlisting(request):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""
    """ didint complete aution info view etc """
     # list of products available
    products = AuctionList.objects.filter(status = False)
    print(products)
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": products,
        "empty": empty,
        "watcher_count" : obj_count
    })

@login_required(login_url='/login')
def mydetailpage(request):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""
  
    return render(request, "auctions/mydetailpage.html", {
        "watcher_count" : obj_count
    })

@login_required(login_url='/login')
def createlisting(request):
    """ i should be able to display a model form and get data from the
    user then redirect to active listing page  
    the user should enter the name , description , initial bid, and picture links limited to 5 with alt rext.
    The other info such as date created, owner status should be auto updated.
    In the picture tables case the aution_id should be auto updated
    """
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""
    
    form = AuctionForm(request.POST or None)
    
    if request.method == "POST":
        if request.user.is_authenticated:

            form = AuctionForm(request.POST)

            for field in form:
                print(field.value())
                print(field)

            if form.is_valid():
                obj = form.save(commit=False) # Return an object without saving to the DB
                obj.owner_id = User.objects.get(pk=request.user.id) # Add an author field which will contain current user's id
                print(obj.owner_id)
                obj.save() # Save the final "real form" to the DB
                return HttpResponseRedirect(reverse('activelisting'))

            else:
                print("ERROR : Form is invalid")
                print(form.errors)
    

    
    context ={
        'form':form,
        'watcher_count':obj_count
        }
    return render(request,"auctions/auction_create.html", context)

@login_required(login_url='/login')
def view_listing(request,list_id):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""
    amount_is_less = None
    bids = Bid.objects.filter(auction_id = list_id)

    listing = get_object_or_404(AuctionList,id = list_id)

    status = listing.status
    
    comments = Comments.objects.filter(auction_id = list_id)

    print("Comments",comments)


    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        comment_obj = comment_form.save(commit=False)
        comment_obj.user = User.objects.get(pk=request.user.id)
        comment_obj.auction_id = AuctionList.objects.get(id = list_id)
        comment_obj.save()
        comment_form = CommentForm()
    

    if bids is not None:


        try:
            bidsofuser = Bid.objects.filter(auction_id = list_id,user = request.user)
        except:
            bidsofuser = None



        previous_bid = 0
        largestbid = 0
        largestbidder = None
        for bid in bids:
            if bid.amount > previous_bid:
                largestbid = bid.amount
                largestbidder = bid.user
            previous_bid = bid.amount
            print("bid.user",bid.user)
            print("bid.amount",bid.amount)
        listing.current_largest_bid = largestbid
        listing.save()
        


        print("largestbid",largestbid)
        print("largestbidder",largestbidder)
        print(request.user.username)
        if str(largestbidder) == str(request.user.username) and bidsofuser:
            isuserWinning = True
            print("hey")
        elif bidsofuser:
            isuserWinning = False
        else:
            isuserWinning = None
        
        print("is user WINNING",isuserWinning)
        # print("My bid:",bidsofuser.amount)


        if status:

            bidform = Bidform(request.POST or None)
            

            


            if bidform.is_valid():
                # Return an object without saving to the DB
                obj = bidform.save(commit=False)
                if obj.amount > largestbid and obj.amount > listing.initial_bid:
                    obj.auction_id = AuctionList.objects.get(id = list_id)
                    obj.user = User.objects.get(pk=request.user.id) # Add an author field which will contain current user's id
                    
                    obj.save() # Save the final "real form" to the DB
                    amount_is_less = None
                    bidform = Bidform()

                    bids = Bid.objects.filter(auction_id = list_id)
                    previous_bid = 0
                    largestbid = 0
                    largestbidder = None
                    for bid in bids:
                        if bid.amount > previous_bid :
                            largestbid = bid.amount
                            largestbidder = bid.user
                    previous_bid = bid.amount

                    listing.current_largest_bid = largestbid
                    listing.save()
                    print("bid.user",bid.user)
                    print("bid.amount",bid.amount)

                else:
                    amount_is_less = "the amount is less"
                    bidform = Bidform()
        else:
            bidform = None
            

        
        
    else:

        if status:

            bidform = Bidform(request.POST or None)
            

            amount_is_less = None
            if bidform.is_valid():
                
                # Return an object without saving to the DB
                obj = bidform.save(commit=False)
                if obj.amount > listing.initial_bid:
                    obj.auction_id = AuctionList.objects.get(id = list_id)
                    obj.user = User.objects.get(pk=request.user.id) # Add an author field which will contain current user's id
                    
                    obj.save() # Save the final "real form" to the DB
                    listing.current_largest_bid = obj.amount
                    listing.save()
                    bidform = Bidform()
                    amount_is_less = None


            


            largestbidder = None
            largestbid = None
            bidsofuser = None
            isuserWinning = None

        else:
            bidform = None
            
    
    if bidform is None:
       isuserWinning = None

    context = {
        'listing' : listing,
        'bidform' : bidform,
        'amount_alert' : amount_is_less,
        'largestbidder' : largestbidder,
        'largestbid' : largestbid,
        'userbid' : bidsofuser,
        'isuserWinning' : isuserWinning ,
        'status': status,
        'comment_form':comment_form,
        'comments': comments,
        'watcher_count':obj_count
        
    }
    return render(request,"auctions/listing_page.html",context)

@login_required(login_url='/login')
def add_to_watchlist(request, list_id):
    
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        listing = AuctionList.objects.get(pk=list_id)
        if request.method == "POST":
                listing.watchers.add(user)
                return HttpResponseRedirect(reverse('viewlisting', args=(listing.id,)))

@login_required(login_url='/login')
def delete_from_watchlist(request, list_id):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        listing = AuctionList.objects.get(pk=list_id)
        if request.method == "POST":
                listing.watchers.remove(user)
                return HttpResponseRedirect(reverse('viewlisting', args=(listing.id,)))
@login_required(login_url='/login')
def closebid(request, list_id,largestbidder):
    if request.method == 'POST':
        try:
            winner = User.objects.get(username= largestbidder)
        except:
            winner = "No bids made"
        
        listing = AuctionList.objects.get(pk=list_id)
        if request.method == "POST":
                listing.status = False
                try:
                    listing.winner = winner
                except:
                    listing.winner = None
                listing.save()
                return HttpResponseRedirect(reverse('viewlisting', args=(listing.id,)))
@login_required(login_url='/login')
def delete_comment(request, comment_id,list_id):
    if request.method == 'POST':
        comment =  Comments.objects.get(pk = comment_id)
        comment.delete()
        return HttpResponseRedirect(reverse('viewlisting',args=(list_id,)))

@login_required(login_url='/login')
def watchlist_page(request):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = "" 
    """ didint complete aution info view etc """
     # list of products available
    products = AuctionList.objects.filter(watchers = request.user,status=True)
    closedproducts = AuctionList.objects.filter(watchers = request.user,status=False)
    print(products)
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/watchlistpage.html", {
        "products": products,
        "closedproducts": closedproducts,
        "empty": empty,
        "watcher_count": obj_count
    })


def categorylist_page(request):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""
    """ didint complete aution info view etc """
     # list of products available
    category_list = Category.objects.all()
    # checking if there are any products
    empty = False
    if len(category_list) == 0:
        empty = True
    return render(request, "auctions/categorylist.html", {
        "category_list": category_list,
        "empty": empty,
        "watcher_count": obj_count
    })


def category_view(request,category_id):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""
    """ didint complete aution info view etc """
     # list of products available
    categoryname=Category.objects.get(pk=category_id)
    products = AuctionList.objects.filter(category = category_id,status=True)
    closedproducts = AuctionList.objects.filter(category = category_id,status=False)
    print(products)
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/category_detail_view.html", {
        "products": products,
        "closedproducts": closedproducts,
        "empty": empty,
        "categoryname" : categoryname,
        "watcher_count": obj_count
    })

@login_required(login_url='/login')
def mybids_view(request):
    try:
        obj_count = AuctionList.objects.filter(watchers = request.user).count()
    except:
        obj_count = ""
    bid_objects = Bid.objects.filter(user = request.user)
    auctions = set()
    for obj in bid_objects:
        auctions.add(AuctionList.objects.get(pk=obj.auction_id.id))
    auctions = list(auctions)

    return render(request, "auctions/mybids_view.html", {
        "products": auctions,
        "watcher_count" : obj_count
    })

    
