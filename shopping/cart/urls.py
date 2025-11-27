from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='AboutUs'),
    path('contact/',views.contact,name='Contact Us'),
    path('tracker/',views.tracker,name='tracker'),
    path('search/',views.search,name='search'),
    path('products/<int:myid>',views.products,name='products'),
    path('checkout/',views.checkout,name='checkout'),
]