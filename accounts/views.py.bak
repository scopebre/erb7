from django.shortcuts import render, redirect

# Create your views here.
def register(request):
    if request.method == 'POST':
        # Process form data here (e.g., create a new user)
        print("submit")
        return redirect('accounts:register')
    else:
        # return redirect('pages:index')  # Redirect to home page after successful registration
        return render(request, 'accounts/register.html')

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return redirect(request, 'pages:index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')