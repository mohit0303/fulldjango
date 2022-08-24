from django.urls import path
from . import views

#this is for JWT token creation either based on user whn log in or whn page is refreshed
#a token is stored in browser and  to make it secure has a lifespan of 5 10 mints,by refresh token we can store it for 30 days or 1 yr as it whn expire it gv a token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #the below 2 path are for JWT token part
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.getRoutes),
    path('projects/',views.getProjects),  #its not written here but path is 'api/projects' bcz in browser if anyone will use /api/ in url it will come here in api folder
    path('projects/<str:pk>',views.getProject),
]

