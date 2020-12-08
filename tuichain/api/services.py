import stripe

def check_number_lr(request):
    number_lr = 0
    loanrequests = LoanRequest.objects.filter(student=user)

    for loanrequest in loanrequests:
        if (loanrequest.validated and loanrequest.active):
            number_lr += 1
    
    if number_lr >= 1:
        return Response({'error': 'An user cannot create Loan Requests when it has one currently undergoing'}, status=HTTP_400_BAD_REQUEST)

def id_verification_intent():
    stripe.stripe_object.StripeObject().request('post', '/v1/identity/verification_intents', {
        "requested_verifications": ["identity_document","selfie"]
        "return_url": 
    })