def is_staff_required(func):
    def checker(request):
        user = request.user
        if user.is_staff == True:
            func(request)
    return checker
