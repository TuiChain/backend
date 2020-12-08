import stripe

def check_number_lr(request):
    loanrequests = LoanRequest.objects.filter(student=user,active=True,validated=True)
    
    if len(loanrequests) >= 1:
        return Response({'error': 'An user cannot create Loan Requests when it has one currently undergoing'}, status=HTTP_400_BAD_REQUEST)

def id_verification_intent(request):

    stripe.api_key = 'sk_test_51HuGjSEXQQPxxsgPzqENPS8d8oDv3aJOGDPETgSOvLjVeB92uyDTKFcO20mFvHEHqhIObyANxPTZlabKOS2s4tk1009xlf5AxD'
    stripe.api_version = '2020-08-27; identity_beta=v3'

    stripe.stripe_object.StripeObject().request('post', '/v1/identity/verification_intents', {
        'return_url': 'api/loanrequests/new/return', # Path to where we want user to end up after ID verification
        'refresh_url': 'api/loanrequests/new/refresh', # Path to where user will receive new link if it expires or it's consumed
        'requested_verifications': ['identity_document','selfie'],
        'meta_data': { # Meta_data might help us connect an ID verification ID to a specific user
            'user_id': user.id_number,
        }
    })