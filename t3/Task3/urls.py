from django.urls import path
from . import views

urlpatterns = [
    path('scraping/', views.scrap, name="scrap"),
    path('Event_brite_scrap_table/', views.Eventbrite, name="Event_brite_scrap_table"),
    path('insider_scrap_table/', views.insider, name="insider"),

    path('table/',views.res,name='result')
	
]
