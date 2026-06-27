from django.http import HttpResponse

def owner_required(view_func):
    def wrapper(request,*args,**kwargs):
        if (request.user.role != "OWNER" and not request.user.is_superuser):
            return HttpResponse("Owner Access only")
        
        return view_func(request,*args,**kwargs)
    return wrapper