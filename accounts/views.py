from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from farmers.models import FarmerProfile
from consumers.models import ConsumerProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


# from django.shortcuts import render, redirect
# from .forms import UserRegisterForm
# from farmers.models import FarmerProfile
# from consumers.models import ConsumerProfile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data['role']
            phone = form.cleaned_data['phone']

            if role == 'farmer':
                FarmerProfile.objects.create(user=user, phone=phone)
            else:
                ConsumerProfile.objects.create(user=user, phone=phone)

            return redirect('login')   # 🔥 search.html

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'farmer':
            return '/farmer/dashboard/'   # Farmer dashboard URL
        else:
            return '/consumer/search/'   