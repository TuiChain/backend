# ---------------------------------------------------------------------------- #

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from tuichain_ethereum import LoanIdentifier

from tuichain.api.models import Loan
from tuichain.api.services.blockchain import controller

# ---------------------------------------------------------------------------- #


def _get_loan(loan_id):
    loan = Loan.objects.get(id=int(loan_id))
    return controller.loans.get_by_identifier(LoanIdentifier(loan.identifier))


def _transactions_to_response(transactions):
    return Response(
        {"transactions": [{"to": t.to, "data": t.data} for t in transactions]},
        status=HTTP_200_OK,
    )


# ---------------------------------------------------------------------------- #


@api_view(["POST"])
@permission_classes((AllowAny,))
def provide_funds(request):
    """
    Build a sequence of transactions for a user to provide funds to a loan.

    Parameters
    ----------
    loan_id : integer

        The loan's id.

    value_atto_dai : string

        The value to provide, in atto-Dai.
    """

    loan = _get_loan(request.data["loan_id"])

    transactions = loan.user_transaction_builder.provide_funds(
        value_atto_dai=int(request.data["value_atto_dai"])
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def withdraw_funds(request):
    """
    Build a sequence of transactions for a user to withdraw funds previously
    provided to a loan.

    Parameters
    ----------
    loan_id : integer

        The loan's id.

    value_atto_dai : string

        The value to withdraw, in atto-Dai.
    """

    loan = _get_loan(request.data["loan_id"])

    transactions = loan.user_transaction_builder.withdraw_funds(
        value_atto_dai=int(request.data["value_atto_dai"])
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def make_payment(request):
    """
    Build a sequence of transactions for a user to make a payment to the loan.

    Parameters
    ----------
    loan_id : integer

        The loan's id.

    value_atto_dai : string

        The payment's value, in atto-Dai.
    """

    loan = _get_loan(request.data["loan_id"])

    transactions = loan.user_transaction_builder.make_payment(
        value_atto_dai=int(request.data["value_atto_dai"])
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def redeem_tokens(request):
    """
    Build a sequence of transactions for a user to redeem tokens previously
    obtained by funding the loan.

    Parameters
    ----------
    loan_id : integer

        The loan's id.

    amount_tokens : string

        The number of tokens to redeem.
    """

    loan = _get_loan(request.data["loan_id"])

    transactions = loan.user_transaction_builder.redeem_tokens(
        amount_tokens=int(request.data["amount_tokens"])
    )

    return _transactions_to_response(transactions)


# ---------------------------------------------------------------------------- #
