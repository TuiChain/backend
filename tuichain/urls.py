from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from tuichain.api.views import auth, investments, loanrequests

router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/login/', auth.login),
    path('api/auth/signup/', auth.signup),
    path('api/investments/new/', investments.create_investment),
    path('api/loanrequests/new/', loanrequests.create_loan_request)
]