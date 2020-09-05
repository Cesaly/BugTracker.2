from django.urls import path
from debug import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('ticket/<int:id>/', views.info),
    path('signup/', views.register),
    path('newticket/', views.newticket),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('inprogess/<int:id>/', views.inprogress),
    path('invalid/<int:id>/', views.invalid),
    path('finished/<int:id>/', views.finished),
    path('edit/<int:id>/', views.editticket),
    path('authorsview/<int:id>/', views.authorsview),
]