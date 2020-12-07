from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from tuichain.api.views import auth, investments, loanrequests
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

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
    path('api/', include(router.urls)),
    # AUTHENTICATION ROUTES
    path('api/auth/login/', auth.login),
    path('api/auth/signup/', auth.signup),
    # INVESTMENTS ROUTES
    path('api/investments/new/', investments.create_investment),
    # LOAN REQUESTS ROUTES
    path('api/loanrequests/new/', loanrequests.create_loan_request),
    # DOCUMENTATION ROUTES
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]