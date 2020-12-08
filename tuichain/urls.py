from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from tuichain.api.views import auth, users, investments, loanrequests, external
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
import os

schema_view = get_schema_view(
   openapi.Info(
      title="Tuichain API",
      default_version='v1',
      description="API developed for the Tuichain application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="peimasters@tuichain.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()

urlpatterns = [
    path('', RedirectView.as_view(url=os.environ['REDIRECT_URL'])),
    path('api/', include(router.urls)),
    # AUTHENTICATION ROUTES
    path('api/auth/login/', auth.login),
    path('api/auth/signup/', auth.signup),
    # USER ROUTES
    # path('api/users/get/<int:id>/', users.get_user),
    # path('api/users/get/', users.get_user),
    # EXTERNAL ROUTES
    path('api/external/create_verification_intent/', external.request_id_verification),
    # INVESTMENTS ROUTES
    path('api/investments/new/', investments.create_investment),
    path('api/investments/get_personal/', investments.get_personal_investments),
    path('api/investments/get/<int:id>/', investments.get_investment),
    # LOAN REQUESTS ROUTES
    path('api/loanrequests/new/', loanrequests.create_loan_request),
    path('api/loanrequests/get_personal/', loanrequests.get_personal_loan_requests),
    path('api/loanrequests/get_all/', loanrequests.get_all_loan_requests),
    path('api/loanrequests/get/<int:id>/', loanrequests.get_loan_request),
    path('api/loanrequests/get/<int:id>/investments/', loanrequests.get_loan_request_investments),
    # DOCUMENTATION ROUTES
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]