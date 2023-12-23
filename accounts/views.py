from audioop import reverse
from urllib import request
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate
from .models import Profile
from .forms import UserForm, ProfileForm, SignupForm
from products.models import Product
from django.contrib import messages
# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # use 'password1' for the first password field

            # authenticate and login the user
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')  # Adjust the redirect URL as needed
    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)
def profile(request, slug):
    profile = get_object_or_404(Profile, user__username=slug)
    return render(request, 'account/profile.html', {'profile': profile})


def profile_edit(request, slug):
    profile = get_object_or_404(Profile, user__username=slug)

    if request.method == 'POST':
        userform = UserForm(request.POST, instance=profile.user)
        profileform = ProfileForm(request.POST, request.FILES, instance=profile)

        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect(reverse('accounts:profile', kwargs={'slug': slug}))
    else:
        userform = UserForm(instance=profile.user)
        profileform = ProfileForm(instance=profile)

    return render(request, 'account/profile_edit.html', {'userform': userform, 'profileform': profileform})
def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if Profile.objects.filter(user=request.user, product_favorits=pro_fav).exists():  # تم تصحيح اسم الحقل هنا أيضًا
            messages.success(request, 'Already product in favorites list')
        else:
            userprofile = Profile.objects.get(user=request.user)
            userprofile.product_favorits.add(pro_fav)  # تم تصحيح اسم الحقل هنا أيضًا
            messages.success(request, 'Product has been favorited')

    else:
        messages.error(request, 'You must be logged in')

    return redirect('/products/' + str(pro_id))
