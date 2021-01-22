from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from tuichain.api.models import Loan, Profile
from tuichain.api.enums import LoanState
from tuichain.api.services.blockchain import controller
from tuichain_ethereum import Address, LoanIdentifier, LoanPhase
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
import decimal
from datetime import timedelta


def _retrieve_current_price(loan):

    state = loan.get_state()

    if state.phase in [
        LoanPhase.FUNDING,
        LoanPhase.CANCELED,
        LoanPhase.EXPIRED,
    ]:

        return str(10 ** 18)

    elif state.phase == LoanPhase.ACTIVE:

        try:

            atto_dai_per_token = median(
                repeat(sp.price_atto_dai_per_token, sp.amount_tokens)
                for sp in controller.market.get_sell_positions_by_loan(loan)
            )

            return str(atto_dai_per_token)

        except StatisticsError:

            return None

    else:  # state.phase == LoanPhase.FINALIZED

        return state.redemption_value_atto_dai_per_token


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_loan_request(request):
    """
    Create new Loan

    Parameters
    ----------
    school : string

        User's desired school.

    course : string

        User's desired course.

    requested_value_atto_dai : float

        requested_value_atto_dai of money pretended by the user.

    destination : string

        Location of the specified university.

    description : string

        Brief description of the loan request's reason.

    Returns
    -------
    201
        Loan request created successfully.

    400
        Required fields are missing or user already has an undergoing loan request.

    """

    user = request.user

    school = request.data.get("school")
    course = request.data.get("course")
    requested_value_atto_dai = request.data.get("requested_value_atto_dai")
    destination = request.data.get("destination")
    description = request.data.get("description")
    recipient_address = request.data.get("recipient_address")

    if (
        school is None
        or course is None
        or requested_value_atto_dai is None
        or destination is None
        or description is None
        or recipient_address is None
    ):
        return Response(
            {
                "error": "Required fields: school, course, requested_value_atto_dai, destination, description and recipient address"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    try:
        Address(recipient_address)
    except ValueError as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

    # TODO: verify if User has complete profile and validated identity

    q = Loan.objects.filter(student=user)
    q = q.exclude(state=LoanState.WITHDRAWN.value)
    loans = q.exclude(state=LoanState.REJECTED.value)

    if len(loans) >= 1:
        return Response(
            {
                "error": "An user cannot create Loan Requests when it has one currently undergoing"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    # ...

    loan = Loan.objects.create(
        student=user,
        school=school,
        course=course,
        requested_value_atto_dai=requested_value_atto_dai,
        destination=destination,
        description=description,
        recipient_address=recipient_address,
    )
    loan.save()

    return Response(
        {"message": "Loan Request successfully created", "loan": loan.id},
        status=HTTP_201_CREATED,
    )


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def cancel_loan(request, id):
    """
    Cancel a Loan

    Parameters
    ----------
    id : integer

        Loan's identifier.

    Returns
    -------
    200
        Loan canceled successfully.

    403
        Cannot cancel a loan that you don't own

    403
        Loan cannot be canceled.

    404
        Loan not found.

    """
    user = request.user
    loan = Loan.objects.filter(id=id).first()

    if loan is None:
        return Response({"error": "Unexistent Loan"}, status=HTTP_404_NOT_FOUND)

    if user != loan.student and not user.is_superuser:
        return Response(
            {"error": "Cannot cancel a loan that you don't own"},
            status=HTTP_403_FORBIDDEN,
        )

    if loan.state != LoanState.APPROVED.value:
        return Response(
            {"error": "The given Loan cannot be canceled"},
            status=HTTP_403_FORBIDDEN,
        )

    controller.loans.get_by_identifier(LoanIdentifier(loan.identifier)).cancel()

    return Response({"message": "Loan has been canceled"}, status=HTTP_200_OK)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def withdraw_loan_request(request, id):
    """
    Withdraw a pending Loan Request

    Parameters
    ----------
    id : integer

        Loan's identifier.

    Returns
    -------
    200
        Loan withdrawn with sucess.

    400
        Loan cannot be withdrawn.

    403
        Loan exists but does not belong to current logged user.

    404
        Loan doesn't exist.

    """

    user = request.user

    loan = Loan.objects.filter(id=id).first()

    if loan is None:
        return Response(
            {"error": "Unexistent Loan Request"}, status=HTTP_404_NOT_FOUND
        )

    if loan.student != user:
        return Response(
            {"error": "Loan Request does not belong to logged user"},
            status=HTTP_403_FORBIDDEN,
        )

    if loan.state > LoanState.PENDING.value:
        return Response(
            {"error": "That Loan Request cannot be withdrawn"},
            status=HTTP_400_BAD_REQUEST,
        )

    # set status as withdrawn
    loan.state = LoanState.WITHDRAWN.value
    loan.save()

    return Response(
        {"message": "Loan Request has been withdrawn"}, status=HTTP_200_OK
    )


@api_view(["PUT"])
@permission_classes((IsAdminUser,))
def validate_loan_request(request, id):
    """
    Validate a Loan Request

    Parameters
    ----------
    id : integer

        Loan request's identifier.

    Returns
    -------
    200
        Loan request validated successfully.

    400
        Loan request fields are missing.

    403
        Loan request has already been validated.

    404
        Unexistent loan request.

    """
    days_to_expiration = request.data.get("days_to_expiration")
    funding_fee_atto_dai_per_dai = request.data.get(
        "funding_fee_atto_dai_per_dai"
    )
    payment_fee_atto_dai_per_dai = request.data.get(
        "payment_fee_atto_dai_per_dai"
    )

    if (
        days_to_expiration is None
        or funding_fee_atto_dai_per_dai is None
        or payment_fee_atto_dai_per_dai is None
    ):
        return Response(
            {
                "error": "Required fields: days_to_expiration, funding_fee_atto_dai_per_dai and payment_fee_atto_dai_per_dai"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    loan = Loan.objects.filter(id=id).first()

    if loan is None:
        return Response(
            {"error": "Unexistent Loan Request"}, status=HTTP_404_NOT_FOUND
        )

    if (
        loan.state > LoanState.CREATING.value
        and loan.state <= LoanState.REJECTED.value
    ):
        return Response(
            {
                "error": "The given Loan Request as already been validated, rejected or withdrawn"
            },
            status=HTTP_403_FORBIDDEN,
        )

    try:
        time_to_expiration = timedelta(days=int(days_to_expiration))
    except Exception as e:
        return Response(
            {
                "error": str(e),
            },
            status=HTTP_400_BAD_REQUEST,
        )

    result = controller.loans.create(
        recipient_address=Address(loan.recipient_address),
        time_to_expiration=time_to_expiration,
        funding_fee_atto_dai_per_dai=int(funding_fee_atto_dai_per_dai),
        payment_fee_atto_dai_per_dai=int(payment_fee_atto_dai_per_dai),
        requested_value_atto_dai=int(loan.requested_value_atto_dai),
    ).get()

    loan.identifier = str(result.identifier)
    loan.state = LoanState.APPROVED.value
    loan.save()

    return Response(
        {"message": "Loan Request has been validated"}, status=HTTP_200_OK
    )


@api_view(["PUT"])
@permission_classes((IsAdminUser,))
def finalize_loan(request, id):
    """
    Finalize a Loan

    Parameters
    ----------
    id : integer

        Loan's identifier.

    Returns
    -------
    200
        Loan finalized successfully.

    403
        Loan cannot be finalized.

    404
        Loan not found.

    """

    loan = Loan.objects.filter(id=id).first()

    if loan is None:
        return Response({"error": "Unexistent Loan"}, status=HTTP_404_NOT_FOUND)

    if loan.state != LoanState.APPROVED.value:
        return Response(
            {"error": "The given Loan cannot be finalized"},
            status=HTTP_403_FORBIDDEN,
        )

    controller.loans.get_by_identifier(
        LoanIdentifier(loan.identifier)
    ).finalize()

    return Response({"message": "Loan has been finalized"}, status=HTTP_200_OK)


@api_view(["PUT"])
@permission_classes((IsAdminUser,))
def reject_loan_request(request, id):
    """
    Reject a Loan request

    Parameters
    ----------
    id : integer

        Loan request's identifier.

    Returns
    -------
    200
        Loan request rejected successfully.

    403
        Loan request already rejected, already been validated or withdrawn by the user.

    404
        Loan request not found.

    """

    loan = Loan.objects.filter(id=id).first()

    if loan is None:
        return Response(
            {"error": "Unexistent Loan request"}, status=HTTP_404_NOT_FOUND
        )

    if loan.state == LoanState.REJECTED.value:
        return Response(
            {"error": "The given Loan request as already been rejected"},
            status=HTTP_403_FORBIDDEN,
        )

    if loan.state > LoanState.PENDING.value:
        return Response(
            {
                "error": "The given Loan request as already been validated or withdrawn by the user"
            },
            status=HTTP_403_FORBIDDEN,
        )

    loan.state = LoanState.REJECTED.value
    loan.save()

    return Response(
        {"message": "Loan request has been rejected"}, status=HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_loan(request, id):
    """
    Get Loan with given ID

    Parameters
    ----------
    id : integer

        Loan's identifier.

    Returns
    -------
    200
        Loan found with success.

    404
        Loan not found.

    """

    loan = Loan.objects.filter(id=id).first()

    # TODO: should we pass it only if it is validated?

    if loan is None:
        return Response(
            {"error": "Loan with given ID not found"},
            status=HTTP_404_NOT_FOUND,
        )

    loan_dict = loan.to_dict()

    if loan.state == LoanState.APPROVED.value:
        fetched_loan = controller.loans.get_by_identifier(
            LoanIdentifier(loan.identifier)
        )
        loan_state = fetched_loan.get_state()
        loan_funding_fee = fetched_loan.funding_fee_atto_dai_per_dai
        loan_payment_fee = fetched_loan.payment_fee_atto_dai_per_dai

        loan_dict["state"] = loan_state.phase.name
        loan_dict["funded_value_atto_dai"] = str(
            loan_state.funded_value_atto_dai
        )
        loan_dict["funding_fee_atto_dai_per_dai"] = str(loan_funding_fee)
        loan_dict["payment_fee_atto_dai_per_dai"] = str(loan_payment_fee)
        loan_dict["current_value_atto_dai"] = _retrieve_current_price(
            fetched_loan
        )
        loan_dict["token_address"] = str(fetched_loan.token_contract_address)

    return Response(
        {
            "message": "Loan found with success",
            "loan": loan_dict,
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_personal_loans(request):
    """
    Get Loan made by the authenticated user

    Parameters
    ----------

    Returns
    -------
    200
        Loans made by authenticated user fetched with success.

    """

    user = request.user

    loan_list = Loan.objects.filter(student=user)
    result = []

    for obj in loan_list:

        loan_dict = obj.to_dict()

        if obj.state == LoanState.APPROVED.value:
            fetched_loan = controller.loans.get_by_identifier(
                LoanIdentifier(obj.identifier)
            )
            state = fetched_loan.get_state()

            loan_dict["state"] = state.phase.name
            loan_dict["current_value_atto_dai"] = _retrieve_current_price(
                fetched_loan
            )
            loan_dict["funded_value_atto_dai"] = state.funded_value_atto_dai
            loan_dict["token_address"] = str(
                fetched_loan.token_contract_address
            )
        result.append(loan_dict)

    return Response(
        {
            "message": "Loan fetched with success",
            "loans": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all_loans(request):
    """
    Get all loans

    Parameters
    ----------

    Returns
    -------
    200
        All Loans fetched with success.

    """

    loan_list = Loan.objects.all()
    result = []

    for obj in loan_list:
        loan_dict = obj.to_dict()
        if obj.state == LoanState.APPROVED.value:
            fetched_loan = controller.loans.get_by_identifier(
                LoanIdentifier(obj.identifier)
            )
            phase = fetched_loan.get_state().phase

            loan_dict["state"] = phase.name
            loan_dict["current_value_atto_dai"] = _retrieve_current_price(
                fetched_loan
            )
        result.append(loan_dict)

    return Response(
        {
            "message": "Loan fetched with success",
            "loans": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_operating_loans(request):
    """
    Get all operating loans

    Parameters
    ----------

    Returns
    -------
    200
        All operating Loans fetched with success.

    """

    q = Loan.objects.exclude(state=LoanState.WITHDRAWN.value)
    loan_list = q.exclude(state=LoanState.REJECTED.value)

    result = []

    for obj in loan_list:
        loan_dict = obj.to_dict()
        if obj.state != LoanState.APPROVED.value:
            result.append(loan_dict)
        else:
            fetched_loan = controller.loans.get_by_identifier(
                LoanIdentifier(obj.identifier)
            )
            phase = fetched_loan.get_state().phase

            if phase not in [LoanPhase.CANCELED, LoanPhase.EXPIRED]:
                loan_dict["state"] = phase.name
                loan_dict["current_value_atto_dai"] = _retrieve_current_price(
                    fetched_loan
                )
                result.append(loan_dict)

    return Response(
        {
            "message": "Loans fetched with success",
            "loans": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_specific_state_loans(request, state, user_info):
    """
    Get all loans at a given state with respective user_info, if requested.

    Parameters
    ----------
    state : integer

        Loan's state.

    user_info : integer

        Flag that tells if information about user should be used or not.

    Returns
    -------
    200
        Loans at given state fetched with success.

    404
        Loans at given state doesn't exist.


    """
    if state in LoanState.__members__:
        loan_list = Loan.objects.filter(state=getattr(LoanState, state).value)
        result = [obj.to_dict() for obj in loan_list]

    elif state in LoanPhase.__members__:
        identifiers_list = [
            loan.identifier
            for loan in controller.loans.get_all()
            if loan.get_state().phase == getattr(LoanPhase, state)
        ]

        result = []

        for identifier in identifiers_list:
            funded_value = (
                controller.loans.get_by_identifier(identifier)
                .get_state()
                .funded_value_atto_dai
            )
            loan = Loan.objects.filter(identifier=identifier).first()
            loan_dict = loan.to_dict()
            fetched_loan = controller.loans.get_by_identifier(identifier)

            loan_dict["state"] = state
            loan_dict["funded_value_atto_dai"] = str(funded_value)
            loan_dict["current_value_atto_dai"] = _retrieve_current_price(
                fetched_loan
            )
            result.append(loan_dict)

    else:
        return Response(
            {"error": "Unexistent Loan State"}, status=HTTP_404_NOT_FOUND
        )

    if user_info:
        for obj in result:
            profile = Profile.objects.filter(user=obj["student"]).first()
            obj["user_full_name"] = profile.user.get_full_name()

    return Response(
        {
            "message": "Loans fetched with success",
            "loans": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )
