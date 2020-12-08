def check_number_lr(request):
    number_lr = 0
    loanrequests = LoanRequest.objects.filter(student=user)

    for loanrequest in loanrequests:
        if (loanrequest.validated and loanrequest.active):
            number_lr += 1
    
    if number_lr >= 1:
        return Response({'error': 'An user cannot create Loan Requests when it has one currently undergoing'}, status=HTTP_400_BAD_REQUEST)