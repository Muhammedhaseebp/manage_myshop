from django.http import HttpResponse

def owner_or_superuser_required(view_func):
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == "OWNER"
        ):
            return view_func(request, *args, **kwargs)

        return HttpResponse("Owner Access Only")

    return wrapper