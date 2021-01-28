from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from tuichain.api.models import Loan, Profile
from tuichain.api.views.loans import _retrieve_current_price
from itertools import chain

from tuichain_ethereum import LoanIdentifier, Address
from tuichain.api.services.blockchain import controller

# ---------------------------------------------------------------------------- #


def _get_loan(loan_id):
    loan = Loan.objects.get(id=int(loan_id))
    return controller.loans.get_by_identifier(LoanIdentifier(loan.identifier))


# ---------------------------------------------------------------------------- #


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_personal_investments(request, user_addr):
    """
    Get Investments made by the authenticated user

    Parameters
    ----------
    user_addr : string

        User's blockchain string address

    Returns
    -------
    200
        Personal investments fetched with success.

    """

    adr = Address(user_addr)

    loans_arr = []
    invested_loans = []

    loan_identifiers = frozenset(
        chain(
            (
                loan.identifier
                for loan in controller.loans.get_by_token_holder(adr)
            ),
            (
                sp.loan.identifier
                for sp in controller.market.get_sell_positions_by_seller(adr)
            ),
        )
    )

    for loan_id in loan_identifiers:

        l = controller.loans.get_by_identifier(loan_id)

        student_id = (
            Loan.objects.filter(identifier=str(l.identifier)).first().student
        )

        student_name = Profile.objects.filter(user=student_id).first().full_name
        loan_dict = (
            Loan.objects.filter(identifier=str(l.identifier)).first().to_dict()
        )
        loan_dict["state"] = l.get_state().phase.name
        loan_dict["current_value_atto_dai"] = _retrieve_current_price(l)

        sell_position = controller.market.get_sell_position_by_loan_and_seller(
            l, adr
        )

        price_per_token_market = 0
        nrTokens_market = 0
        if sell_position is not None:
            nrTokens_market = sell_position.amount_tokens
            price_per_token_market = sell_position.price_atto_dai_per_token

        loan_obj = {
            "loan": loan_dict,
            "name": student_name,
            "nrTokens": l.get_token_balance_of(adr),
            "nrTokens_market": nrTokens_market,
            "price_per_token_market": price_per_token_market,
        }

        loans_arr.append(loan_obj)

    return Response(
        {
            "message": "Personal investments fetched with success",
            "investments": loans_arr,
            "count": len(loans_arr),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_investment(request, id, user_addr):
    """
    Get Investment with the given ID

    Parameters
    ----------
    loan_id : integer

        Loan's database identifier.

    user_addr : string

        User blockchain address

    Returns
    -------
    200
        Investments fetched with success.

    """

    adr = Address(user_addr)

    loan = _get_loan(id)

    student_id = (
        Loan.objects.filter(identifier=str(loan.identifier)).first().student
    )
    student_name = Profile.objects.filter(user=student_id).first().full_name

    loan_dict = (
        Loan.objects.filter(identifier=str(loan.identifier)).first().to_dict()
    )
    loan_dict["state"] = loan.get_state().phase.name

    sell_position = controller.market.get_sell_position_by_loan_and_seller(
            loan, adr
        )

    price_per_token_market = 0
    nrTokens_market = 0
    if sell_position is not None:
        nrTokens_market = sell_position.amount_tokens
        price_per_token_market = sell_position.price_atto_dai_per_token

    loan_obj = {
        "loan": loan_dict,
        "name": student_name,
        "nrTokens": loan.get_token_balance_of(adr),
        "nrTokens_market": nrTokens_market,
        "price_per_token_market": price_per_token_market,
    }

    return Response(
        {
            "message": "Investment fetched with success",
            "investment": loan_obj,
        },
        status=HTTP_200_OK,
    )

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_general_investments(request, id):
    """
    Get Investment with the given ID

    Parameters
    ----------
    loan_id : integer

        Loan's database identifier.

    Returns
    -------
    200
        Investments fetched with success.

    """

    loan = _get_loan(id)

    student_id = (
        Loan.objects.filter(identifier=str(loan.identifier)).first().student
    )
    student_name = Profile.objects.filter(user=student_id).first().full_name

    loan_dict = (
        Loan.objects.filter(identifier=str(loan.identifier)).first().to_dict()
    )
    loan_dict["state"] = loan.get_state().phase.name

    sell_positions = controller.market.get_sell_positions_by_loan(loan)

    sp_list = []
    #for sp in sell_positions:
    #    if sp is not None:
    #        sp_list.add(sp)
    for sp in sell_positions:
        sp_list.append(sp)

    loan_obj = {
        "loan": loan_dict,
        "name": student_name,
        #"nrTokens": loan.get_token_balance_of(adr),
        "sell_positions": sp_list,
    }

    return Response(
        {
            "message": "Investment fetched with success",
            "investment": loan_obj,
        },
        status=HTTP_200_OK,
    )

# ---------------------------------------------------------------------------- #
