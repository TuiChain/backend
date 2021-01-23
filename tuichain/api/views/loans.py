from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from tuichain.api.models import Loan, Profile, Document
from tuichain.api.enums import LoanState
from tuichain.api.services.blockchain import controller
from tuichain.api.services.storage import upload_file
from tuichain_ethereum import Address, LoanIdentifier, LoanPhase
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
import decimal
from datetime import timedelta, datetime


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
        {"message": "Loan Request successfully created"},
        status=HTTP_201_CREATED,
    )


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
    201
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
        {"message": "Loan Request has been withdrawn"}, status=HTTP_201_CREATED
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
    201
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
        {"message": "Loan Request has been validated"}, status=HTTP_201_CREATED
    )


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
    201
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
        {"message": "Loan request has been rejected"}, status=HTTP_201_CREATED
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

        loan_dict["state"] = loan_state.phase.name
        loan_dict["funded_value_atto_dai"] = loan_state.funded_value_atto_dai
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
            phase = (
                controller.loans.get_by_identifier(
                    LoanIdentifier(obj.identifier)
                )
                .get_state()
                .phase
            )
            loan_dict["state"] = phase.name
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
            phase = (
                controller.loans.get_by_identifier(
                    LoanIdentifier(obj.identifier)
                )
                .get_state()
                .phase
            )
            loan_dict["state"] = phase.name
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
            loan = controller.loans.get_by_identifier(
                LoanIdentifier(obj.identifier)
            )
            phase = loan.get_state().phase
            if phase not in [LoanPhase.CANCELED, LoanPhase.EXPIRED]:
                loan_dict["state"] = phase.name
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
            loan = Loan.objects.filter(identifier=identifier).first()
            loan_dict = loan.to_dict()
            loan_dict["state"] = state
            result.append(loan_dict)

    else:
        return Response(
            {"error": "Unexistent Loan State"}, status=HTTP_404_NOT_FOUND
        )

    if user_info:
        for obj in result:
            user = Profile.objects.filter(user=obj["student"]).first()
            obj["user_full_name"] = user.full_name

    return Response(
        {
            "message": "Loans fetched with success",
            "loans": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAdminUser,))
def get_loan_unevaluated_docs(request, id):
    """
    Get all unevaluated docs for a given Loan. ADMIN ONLY.

    Parameters
    ----------
    id: integer
        Loan request ID

    Returns
    -------
    200
        Documents fetched with success

    404
        Unexistent Loan Request

    """
    loan = Loan.objects.filter(id=id).first()

    if loan is None:
        return Response(
            {"error": "Unexistent Loan Request"}, status=HTTP_404_NOT_FOUND
        )

    documents = Document.objects.filter(
        loan=loan, approved=False, rejected=False
    )

    result = [doc.to_dict() for doc in documents]

    return Response(
        {
            "message": "Documents fetched with success",
            "loan": id,
            "documents": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_loan_approved_public_docs(request, id):
    """
    Get all approved public docs for a given Loan.

    Parameters
    ----------
    id: integer
        Loan request ID

    Returns
    -------
    200
        Documents fetched with success

    404
        Unexistent Loan Request

    """
    loan = Loan.objects.filter(id=id).first()

    if loan is None:
        return Response(
            {"error": "Unexistent Loan Request"}, status=HTTP_404_NOT_FOUND
        )

    documents = Document.objects.filter(
        loan=loan, is_public=True, approved=True
    )

    result = [doc.to_dict() for doc in documents]

    return Response(
        {
            "message": "Documents fetched with success",
            "loan": id,
            "documents": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_loan_personal_docs(request, id):
    """
    Get all personal docs (private and public) for a given Loan.

    Parameters
    ----------
    id: integer
        Loan request ID

    Returns
    -------
    200
        Documents fetched with success

    403
        Loan Request does not belong to logged user

    404
        Unexistent Loan Request

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

    documents = Document.objects.filter(loan=id)

    result = [doc.to_dict() for doc in documents]

    return Response(
        {
            "message": "Documents fetched with success",
            "loan": id,
            "documents": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes((IsAdminUser,))
def get_all_unevaluated_documents(request):
    """
    Get all unevaluated docs for all the Loans. ADMIN ONLY.

    Returns
    -------
    200
        Documents fetched with success

    """
    documents = Document.objects.filter(approved=False, rejected=False)

    result = [doc.to_dict() for doc in documents]

    return Response(
        {
            "message": "Documents fetched with success",
            "documents": result,
            "count": len(result),
        },
        status=HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes((IsAdminUser,))
def approve_document(request, id):
    """
    Approve document with given ID. ADMIN ONLY.

    Parameters
    ----------
    id: integer
        Document ID

    Returns
    -------
    201
        Document approved with success

    404
        Document Not Found

    """
    document = Document.objects.filter(id=id).first()

    if document is None:
        return Response(
            {"error": "Document Not Found"},
            status=HTTP_404_NOT_FOUND,
        )

    document.approved = True
    document.rejected = False

    document.save()

    return Response(
        {
            "message": "Document approved with success",
            "document": document.to_dict(),
        },
        status=HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes((IsAdminUser,))
def reject_document(request, id):
    """
    Reject document with given ID. ADMIN ONLY.

    Parameters
    ----------
    id: integer
        Document ID

    Returns
    -------
    201
        Document rejected with success

    404
        Document Not Found

    """
    document = Document.objects.filter(id=id).first()

    if document is None:
        return Response(
            {"error": "Document Not Found"},
            status=HTTP_404_NOT_FOUND,
        )

    document.approved = False
    document.rejected = True

    document.save()

    return Response(
        {
            "message": "Document rejected with success",
            "document": document.to_dict(),
        },
        status=HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def upload_document(request, id):
    """
    Upload document for the Loan with the given ID.

    Parameters
    ----------
    id: integer
        Loan ID

    Returns
    -------
    201
        Document uploaded with success

    400
        Required fields: document, name and is_public

    403
        Loan Request does not belong to logged user

    404
        Unexistent Loan Request

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

    document = request.data.get("document")
    name = request.data.get("name")
    is_public = request.data.get("is_public")

    if document is None or name is None or is_public is None:
        return Response(
            {"error": "Required fields: document, name and is_public"},
            status=HTTP_400_BAD_REQUEST,
        )

    url = upload_file(
        document,
        "loan_"
        + str(id)
        + "_"
        + name
        + "_"
        + str(round(datetime.now().timestamp())),
    )

    doc = Document.objects.create(
        loan=loan,
        name=name,
        is_public=is_public,
        approved=False,
        url=url,
    )
    doc.save()

    return Response(
        {
            "message": "Document uploaded with success",
            "document": doc.to_dict(),
        },
        status=HTTP_201_CREATED,
    )
