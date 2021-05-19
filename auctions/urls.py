from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activelisting", views.activelisting, name="activelisting"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("watchlistpage", views.watchlist_page, name="watchlistpage"),
    path("mydetailpage", views.mydetailpage, name="mydetailpage"),
    path("categorylist", views.categorylist_page, name="categorylistpage"),
    path("category_view/<int:category_id>", views.category_view, name="category_view"),
    path("mybids_view", views.mybids_view, name="mybids_view"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<int:list_id>",views.view_listing,name="viewlisting"),
    path("add_to_watchlist/<int:list_id>",views.add_to_watchlist,name="add_to_watchlist"),
    path("delete_from_watchlist/<int:list_id>",views.delete_from_watchlist,name="delete_from_watchlist"),
    path("closebid/<int:list_id>/<str:largestbidder>/",views.closebid,name="closebid"),
    path("delete_comment/<int:comment_id>/<int:list_id>/",views.delete_comment,name="delete_comment")
]
