from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    #function based views
    #path('', views.home, name='home'),
    #path('detail/<int:id>', views.detail, name='detail'),

    #class based views
    path('', views.HomePageView.as_view(), name='home'),
    path('detail/<int:pk>', views.ContactDetailView.as_view(), name='detail'),
    path('search/', views.search, name='search'),
    path('contacts/create', views.ContactCreateView.as_view(), name='create'),
    path('contacts/update/<int:pk>', views.ContactUpdateView.as_view(), name='update'),
    path('contacts/delete/<int:pk>', views.ContactDeleteView.as_view(), name='delete'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
