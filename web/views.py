from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # username = request.POST.get('username', None)
        # password = request.POST.get('password', None)

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request , user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request , "There was an Error to Logging in , Please try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records' : records})
    
def logout_user(request):
    logout(request)
    messages.success(request , 'you have been logged out')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # authenticate() check user in db (founded) or (new)
            # (founded) it return it
            # (new) it return (None)
            user = authenticate(username=username, password=password)
            
            if user is not None: # new user register
                login(request, user)
                messages.success(request, 'You have successfully registered!')
                return redirect('home')
            else: # founded user register
                messages.error(request, 'Authentication failed.')
                return render(request, 'register.html', {'form': form})
            
        else:
            # Form is invalid; re-render the template with errors
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})


def customer_record(request , pk):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        
        # look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'You Must Be Logged In To View That Page!')
        return redirect('home')

def delete_record(request , pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record Deleted Successfully')
        return redirect('home')
    else:
        messages.success(request , 'You Must Be Logged In')
        return redirect('home')



def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record Added')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})

    else:
        messages.success(request, 'Ypu Must be Logged In..!')
        return redirect('home')

def update_record(request , pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None , instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Has Been Updated !!')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You Must Logged In...!!')
        return redirect('home')






