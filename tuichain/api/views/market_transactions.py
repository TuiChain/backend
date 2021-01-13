# ---------------------------------------------------------------------------- #

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from tuichain_ethereum import Address, LoanIdentifier

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
def create_sell_position(request):
    """
    Build a sequence of transactions for a user to create a sell position.

    Parameters
    ----------
    loan_id : integer

        The identifier of the loan whose token the sell position refers to.

    amount_tokens : string

        The number of tokens to offer.

    price_atto_dai_per_token : string

        The price, in atto-Dai per token.
    """

    builder = controller.market.user_transaction_builder

    transactions = builder.create_sell_position(
        loan=_get_loan(request.data["loan_id"]),
        amount_tokens=int(request.data["amount_tokens"]),
        price_atto_dai_per_token=int(request.data["price_atto_dai_per_token"]),
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def remove_sell_position(request):
    """
    Build a sequence of transactions for a user to remove an existing sell
    position.

    Parameters
    ----------
    loan_id : integer

        The identifier of the loan whose token the sell position refers to.
    """

    builder = controller.market.user_transaction_builder

    transactions = builder.remove_sell_position(
        loan=_get_loan(request.data["loan_id"])
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def increase_sell_position_amount(request):
    """
    Build a sequence of transactions for a user to increase the token amount of
    an existing sell position.

    Parameters
    ----------
    loan_id : integer

        The identifier of the loan whose token the sell position refers to.

    increase_amount : string

        The number of tokens to add to the amount offered by the sell position.
    """

    builder = controller.market.user_transaction_builder

    transactions = builder.increase_sell_position_amount(
        loan=_get_loan(request.data["loan_id"]),
        increase_amount=int(request.data["increase_amount"]),
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def decrease_sell_position_amount(request):
    """
    Build a sequence of transactions for a user to decrease the token amount of
    an existing sell position.

    Parameters
    ----------
    loan_id : integer

        The identifier of the loan whose token the sell position refers to.

    decrease_amount : string

        The number of tokens to subtract from the amount offered by the sell
        position.
    """

    builder = controller.market.user_transaction_builder

    transactions = builder.decrease_sell_position_amount(
        loan=_get_loan(request.data["loan_id"]),
        decrease_amount=int(request.data["decrease_amount"]),
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def update_sell_position_price(request):
    """
    Build a sequence of transactions for a user to update the price of an
    existing sell position.

    Parameters
    ----------
    loan_id : integer

        The identifier of the loan whose token the sell position refers to.

    new_price_atto_dai_per_token : string

        The new price, in atto-Dai per token.
    """

    builder = controller.market.user_transaction_builder

    transactions = builder.update_sell_position_price(
        loan=_get_loan(request.data["loan_id"]),
        new_price_atto_dai_per_token=int(
            request.data["new_price_atto_dai_per_token"]
        ),
    )

    return _transactions_to_response(transactions)


@api_view(["POST"])
@permission_classes((AllowAny,))
def purchase(request):
    """
    Build a sequence of transactions for a user to purchase tokens from an
    existing sell position.

    Parameters
    ----------
    loan_id : integer

        The identifier of the loan whose token the sell position refers to.

    seller_address : string

        The address of the seller.

    amount_tokens : string

        The number of tokens to offer.

    price_atto_dai_per_token : string

        The price, in atto-Dai per token.

    fee_atto_dai_per_nano_dai : string

        The market purchase fee, in atto-Dai per paid nano-Dai.
    """

    builder = controller.market.user_transaction_builder

    transactions = builder.purchase(
        loan=_get_loan(request.data["loan_id"]),
        seller_address=Address(request.data["seller_address"]),
        amount_tokens=int(request.data["amount_tokens"]),
        price_atto_dai_per_token=int(request.data["price_atto_dai_per_token"]),
        fee_atto_dai_per_nano_dai=int(
            request.data["fee_atto_dai_per_nano_dai"]
        ),
    )

    return _transactions_to_response(transactions)


# ---------------------------------------------------------------------------- #
