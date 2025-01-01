# D:\PROJECT\PLACEU final\place_u\decorators.py

from django.shortcuts import redirect

def admin_or_tech_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if user is logged in as admin or tech
        if 'admin' in request.session or 'ad_no' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to the appropriate login page
            if 'admin' in request.path:
                return redirect('adminlogin')
            else:
                return redirect('techlogin')
    return wrapper
