from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import allowed_users, haveFaces, cropper
from .forms import ApplicationForm
from .models import Application
from django.contrib import messages


# Create your views here.


@login_required(login_url='Auth:login')
@allowed_users(allowed_roles=['customer'])
def dashboard(request):
    user = request.user
    customer = User.objects.get(username=user)

    form = ApplicationForm(instance=customer)
    prevApp = Application.objects.filter(customer=user)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            user = form.save()
            fName = form.cleaned_data.get('fName')
            lName = form.cleaned_data.get('lName')
            image = form.cleaned_data.get('images')

            application = Application(fName=fName, lName=lName, images=image, customer=user)
            application.save()

            ret, cord = haveFaces(application.images.name)

            if ret:
                cropper(application.images.name, cord)
                messages.success(request, f'Applied successfully for {fName} {lName}!')
            else:
                application.delete()
                messages.error(request, f'Application failed! Upload image containing face of only one person.')

        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {errors}')

        return redirect('Customer:dashboard')

    return render(request, "customer/dashboard.html", {'Customer': customer, 'form': form, 'prevApp': prevApp})


@login_required(login_url='Auth:login')
@allowed_users(allowed_roles=['customer'])
def changeStatus(request):
    if request.method == 'POST':
        appId = request.POST.get('appId')
        Application.objects.get(appId=appId).delete()
        messages.success(request, f'Removed successfully!')

    return redirect('Customer:dashboard')
