from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from tuichain.api.views import (
    auth,
    users,
    investments,
    loans,
    external,
    blockchain,
    loan_transactions,
    market_transactions,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

# schema_view = get_schema_view(
#     openapi.Info(
#       title="Tuichain API",
#       default_version='v1',
#       description="API developed for the Tuichain application",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="peimasters@tuichain.com"),
#       license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

router = routers.DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    # AUTHENTICATION ROUTES
    path("api/auth/login/", auth.login),
    path("api/auth/signup/", auth.signup),
    path("api/auth/verify_email/", auth.verify_email),
    path("api/auth/verify_username/", auth.verify_username),
    path("api/auth/reset_password/<int:id>/<str:token>/", auth.reset_password),
    path("api/auth/email_reset_password/", auth.email_reset_password),
    path("api/auth/is_admin/", auth.is_admin_user),
    # USER ROUTES
    path("api/users/get/<int:id>/", users.get_user),
    path("api/users/get/", users.get_me),
    path("api/users/get_all/", users.get_all),
    path("api/users/update_profile/", users.update_profile),
    # BLOCKCHAIN ROUTES
    path("api/tuichain/get_info/", blockchain.get_blockchain_info),
    # EXTERNAL ROUTES
    path(
        "api/external/create_verification_intent/",
        external.request_id_verification,
    ),
    path(
        "api/external/get_verification_intent/<slug:verification_intent_id>",
        external.get_id_verification_result,
    ),
    # INVESTMENTS ROUTES
    path("api/investments/new/", investments.create_investment),
    path("api/investments/get_personal/", investments.get_personal_investments),
    path("api/investments/get/<int:id>/", investments.get_investment),
    # LOAN REQUESTS ROUTES
    path("api/loans/new/", loans.create_loan_request),
    path(
        "api/loans/validate/<int:id>/",
        loans.validate_loan_request,
    ),
    path("api/loans/reject/<int:id>/", loans.reject_loan_request),
    path(
        "api/loans/get_personal/",
        loans.get_personal_loans,
    ),
    path("api/loans/get_all/", loans.get_all_loans),
    path("api/loans/get_operating/", loans.get_operating_loans),
    path(
        "api/loans/get_state/<str:state>/<int:user_info>/",
        loans.get_specific_state_loans,
    ),
    path("api/loans/get/<int:id>/", loans.get_loan),
    path(
        "api/loans/user_withdraw/<int:id>/",
        loans.withdraw_loan_request,
    ),
    # USER TRANSACTIONS
    path(
        "api/loans/transactions/provide_funds/",
        loan_transactions.provide_funds,
    ),
    path(
        "api/loans/transactions/withdraw_funds/",
        loan_transactions.withdraw_funds,
    ),
    path(
        "api/loans/transactions/make_payment/", loan_transactions.make_payment
    ),
    path(
        "api/loans/transactions/redeem_tokens/",
        loan_transactions.redeem_tokens,
    ),
    path(
        "api/market/transactions/create_sell_position/",
        market_transactions.create_sell_position,
    ),
    path(
        "api/market/transactions/remove_sell_position/",
        market_transactions.remove_sell_position,
    ),
    path(
        "api/market/transactions/increase_sell_position_amount/",
        market_transactions.increase_sell_position_amount,
    ),
    path(
        "api/market/transactions/decrease_sell_position_amount/",
        market_transactions.decrease_sell_position_amount,
    ),
    path(
        "api/market/transactions/update_sell_position_price/",
        market_transactions.update_sell_position_price,
    ),
    path("api/market/transactions/purchase/", market_transactions.purchase),
    # DOCUMENTATION ROUTES
    re_path(r"^api/docs/", include_docs_urls(title="Tuichain API")),
    #    re_path(
    #        r"^swagger(?P<format>\.json|\.yaml)$",
    #        schema_view.without_ui(cache_timeout=0),
    #        name="schema-json",
    #    ),
    #    re_path(
    #        r"^swagger/$",
    #        schema_view.with_ui("swagger", cache_timeout=0),
    #        name="schema-swagger-ui",
    #    ),
    #    re_path(
    #        r"^redoc/$",
    #        schema_view.with_ui("redoc", cache_timeout=0),
    #        name="schema-redoc",
    #    ),
]
