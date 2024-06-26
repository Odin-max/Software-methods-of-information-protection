from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from users.forms import RegistrationForm,AddUserForm, LoginForm, ChangePasswordForm, CreateUserForm, AdminPasswordChangeForm
from django.contrib import messages
from users.models import User
import time
import re

def is_admin(user):
    return user.role == 1

def contains_required_chars(password):
    has_letter = bool(re.search(r'[a-zA-Z]', password))
    has_arithmetic = bool(re.search(r'[+\-*/]', password))
    return has_letter and has_arithmetic

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(login=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    if user.is_blocked:
                        return render(request, 'index.html', {'form': form, 'error': 'Your account is blocked.'})
                    if user.password_restriction and not contains_required_chars(password):
                        return render(request, 'index.html', {
                            'form': form,
                            'password_form': ChangePasswordForm(user=user),
                            'user_id': user.id,
                            'show_password_modal': True,
                            'error': 'Password must contain both letters and arithmetic symbols.'
                        })

                    request.session['password_attempts'] = 0  # Reset attempts on success
                    login(request, user)  # Login the user to start the session
                    user.last_login = timezone.now()  # Update the last_login field
                    user.save()
                    if user.role == 1:  # Assuming role 1 is superuser
                        return redirect('/admin_panel/')
                    else:
                        return redirect('/user_panel/')
                else:
                    return render(request, 'index.html', {'form': form, 'error': 'Invalid username or password.'})
            except User.DoesNotExist:
                return render(request, 'index.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})

@login_required
def handle_password_change(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ChangePasswordForm(user=user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Your password has been changed successfully. Please log in again.')
            return redirect('login_page')
        else:
            return render(request, 'index.html', {
                'form': LoginForm(),
                'password_form': form,
                'user_id': user.id,
                'show_password_modal': True,
                'error': 'Please correct the errors below.'
            })
    return redirect('login_page')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(login=username)
                if check_password(password, user.password):
                    if user.is_blocked:
                        return render(request, 'index.html', {'form': form, 'error': 'Your account is blocked.'})
                    if user.role == 1:  # Assuming role 1 is superuser
                        return redirect('/admin_panel/')
                    else:
                        return redirect('/user_panel/')
                else:
                    return render(request, 'index.html', {'form': form, 'error': 'Invalid username or password.'})
            except User.DoesNotExist:
                return render(request, 'index.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Hash the password before saving
            hashed_password = make_password(password)
            
            user = User(
                login=username,
                password=hashed_password,  # Store the hashed password
                first_name=first_name,
                last_name=last_name,
                role=0,
            )
            user.save()
            return redirect('login_page')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def forgot_password_page(request):
    return render(request, 'change_pass.html')



@login_required
def admin_panel(request):
    if request.user.role != 1:  # Ensure the user is an admin
        return redirect('login_page')

    # Handle password visibility toggle
    if 'toggle_password_visibility' in request.GET:
        request.session['password_visibility'] = not request.session.get('password_visibility', False)
    
    # Get the password visibility flag from the session
    password_visibility = request.session.get('password_visibility', False)

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = ChangePasswordForm(user=request.user, data=request.POST)
            create_user_form = CreateUserForm()
            if password_form.is_valid():
                new_password = password_form.cleaned_data['new_password']
                user = User.objects.get(id=request.user.id)
                user.password = make_password(new_password)  # Hash the new password
                user.save()  # Save the changes
                messages.success(request, 'Your password was successfully updated!')
                return redirect('admin_panel')
            else:
                messages.error(request, 'Please correct the errors below.')
        elif 'create_user' in request.POST:
            create_user_form = CreateUserForm(request.POST)
            password_form = ChangePasswordForm(user=request.user)
            if create_user_form.is_valid():
                login = create_user_form.cleaned_data['login']
                password = create_user_form.cleaned_data['password']
                first_name = create_user_form.cleaned_data['first_name']
                last_name = create_user_form.cleaned_data['last_name']
                role = create_user_form.cleaned_data['role']
                is_blocked = create_user_form.cleaned_data['is_blocked']
                
                if password:
                    password = make_password(password)  # Hash the password if provided
                else:
                    password = make_password('default_password')  # Provide a default hashed password

                user = User(
                    login=login,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    is_blocked=is_blocked,
                )
                user.save()
                messages.success(request, f'User {login} created successfully!')
                return redirect('admin_panel')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        password_form = ChangePasswordForm(user=request.user)
        create_user_form = CreateUserForm()

    users = User.objects.all()
    return render(request, 'admin.html', {
        'password_form': password_form,
        'create_user_form': create_user_form,
        'users': users,
        'password_visibility': password_visibility,
    })

@login_required
def toggle_password_restriction(request, user_id):
    if request.user.role != 1:
        return redirect('login_page')
    
    user = get_object_or_404(User, id=user_id)
    user.password_restriction = not user.password_restriction
    user.save()
    return redirect('admin_panel')

@user_passes_test(is_admin)
@login_required
def view_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'view_password.html', {'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.user.role == 1:  # Assuming role 1 is superuser
        return redirect('login_page')
    if user.role != 1:  # Ensure the superuser cannot delete themselves or other superusers
        user.delete()
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, 'Cannot delete superuser.')

    return redirect('admin_panel')

@login_required
def admin_change_password(request):
    if request.user.role != 1:  # Ensure the user is an admin
        return redirect('login_page')

    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(id=request.user.id)
            user.password = make_password(new_password)  # Hash the new password
            user.save()  # Save the changes
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'admin_change_password.html', {'form': form})


@login_required
def admin_add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User(login=username, password=make_password('default_password'), first_name='', last_name='', role=0, is_blocked=False)
            user.save()
            return redirect('/admin_panel/')
    else:
        form = AddUserForm()
    return render(request, 'add_user.html', {'form': form})

@login_required
def block_user(request, user_id):
    if not request.user.role == 1:
        return redirect('login')

    user_to_block = get_object_or_404(User, id=user_id)
    user_to_block.is_blocked = True
    user_to_block.save()
    messages.success(request, 'User blocked successfully.')

    return redirect('admin_panel')


@login_required
def unblock_user(request, user_id):
    if not request.user.role == 1:
        return redirect('login')

    user_to_unblock = get_object_or_404(User, id=user_id)
    user_to_unblock.is_blocked = False
    user_to_unblock.save()
    messages.success(request, 'User unblocked successfully.')

    return redirect('admin_panel')

@login_required
def toggle_password_restriction(request, user_id):
    if not request.user.role == 1:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    user.password_restriction = not user.password_restriction
    user.save()
    messages.success(request, 'Password restriction toggled successfully.')

    return redirect('admin_panel')

@login_required
def admin_complete_work(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login_page')
    return render(request, 'admin.html')

# User Panel Views
@login_required
def user_panel(request):
    return render(request, 'user_panel.html')

@login_required
def user_change_password(request):
    if request.user.password_restriction:
        attempts = request.session.get('password_change_attempts', 0)
        cooldown_until = request.session.get('cooldown_until', 0)
        
        if attempts >= 3 and time.time() < cooldown_until:
            messages.error(request, f'Too many failed attempts. Try again after {int((cooldown_until - time.time()) / 60)} minutes.')
            return redirect('user_panel')

    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            if request.user.password_restriction and not contains_required_chars(new_password):
                messages.error(request, 'New password must contain only letters and arithmetic symbols.')
                return redirect('user_change_password')

            user = User.objects.get(id=request.user.id)
            user.password = make_password(new_password)  # Hash the new password
            user.save()  # Save the changes
            request.session['password_change_attempts'] = 0  # Reset attempts on success
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_panel')
        else:
            messages.error(request, 'Please correct the errors below or use a different password.')
            if request.user.password_restriction:
                attempts += 1
                request.session['password_change_attempts'] = attempts
                if attempts >= 3:
                    request.session['cooldown_until'] = time.time() + 15  # 15 seconds cooldown for example
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'user_panel.html', {'form': form})


@login_required
def user_complete_work(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login_page')
    return render(request, 'complete_work.html')
