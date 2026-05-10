from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from portal.form import ApplicationForm, RegistrationForm, LoginForm
from portal.models import Application,Client


def main(request):
    return HttpResponse("SITE WORKS")

def locations(request):
    return render(request, 'portal/locations.html')


def contact(request):
    return render(request, 'portal/contact.html')

@login_required
def profile(request):
    try:
        client = request.user.client
    except:
        return redirect('register')

    applications = Application.objects.filter(client=client)

    return render(
        request,
        'portal/personal_account.html',
        {
            'client': client,
            'applications': applications
        }
    )

@login_required
def apple(request):
    client = request.user.client

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            Application.objects.create(
                client=client,
                plot_size=form.cleaned_data['plot_size'],
                building=form.cleaned_data['building'],
                payment_acquisitions=form.cleaned_data['payment_acquisitions'],
                cadastral_number=form.cleaned_data['cadastral_number'],
                passport_data=form.cleaned_data['passport_data'],
                address=form.cleaned_data['address'],
                document=form.cleaned_data.get('document')
            )

            return redirect('apple')

    else:
        form = ApplicationForm()

    return render(
        request,
        'portal/apple.html',
        {'form': form}
    )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ВСЕ пользовательские данные сюда
            Client.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone']
            )

            login(request, user)
            return redirect('main')
    else:
        form = RegistrationForm()

    return render(request, 'portal/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main')
    else:
        form = LoginForm()

    return render(request, 'portal/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('main')
