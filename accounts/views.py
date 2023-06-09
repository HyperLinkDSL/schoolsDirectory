from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, FormView, DeleteView, ListView, CreateView
from accounts.models import Profile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from accounts.utils import get_all_perms, selected_perms
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.forms import CreateProfileForm, UpdateProfileForm, SignUpForm, RequestPasswordResetForm, ResetPasswordForm
from django.contrib.auth.models import Permission

from tokens import account_activation_token


class ListProfiles(PermissionRequiredMixin, ListView):
    model = Profile
    template_name = "accounts/list_profiles.html"
    raise_exception = True
    permission_required = ['profile.view_profile']
    permission_denied_message = "You don't have permission to view profiles"
    paginate_by = 20


class SetPermissions(PermissionRequiredMixin, FormView):
    template_name = 'accounts/set_permissions.html'
    perms_list = get_all_perms()

    def has_permission(self):

        # only allow superuser to access this view
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):

        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        profile_perms_query = profile.user_permissions.all()
        profile_perms = [profile_perm.codename for profile_perm in profile_perms_query]

        context = {
            'perms_list': self.perms_list,
            'profile_perms_query': profile_perms_query,
            'profile_perms': profile_perms,
            'profile': profile,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])

        perms_selected = selected_perms(form_data=request.POST)
        profile_perms_query = profile.user_permissions.all()
        profile_perms = [profile_perm.codename for profile_perm in profile_perms_query]

        # remove existing perm that is not selected
        for perm in profile_perms:
            if perm not in perms_selected:
                profile.user_permissions.remove(
                    Permission.objects.get(codename=perm)
                )

        # add new selected perm
        for perm in perms_selected:
            if perm not in profile_perms:
                profile.user_permissions.add(
                    Permission.objects.get(codename=perm)
                )

        messages.success(request, f"Success, updated permissions for {profile.last_name}", extra_tags="alert alert-success")

        return redirect(to=f"/profile/set-permissions/{profile.pk}/")


class UpdatePassword(PermissionRequiredMixin, FormView):
    permission_denied_message = "You dont have permission to change profile"
    raise_exception = True
    form_class = PasswordChangeForm

    def has_permission(self):

        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])

        # Allow logged-in user or superuser to change password
        if profile.pk == self.request.user.pk or self.request.user.is_superuser:
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):

        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])

        form = self.form_class(user=profile, data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Success, password updated', extra_tags='alert alert-success')
        else:
            messages.error(request, 'Failed, password NOT updated', extra_tags='alert alert-danger')

        return redirect(to='profile:update-profile', pk=self.kwargs['pk'])


class DeleteProfile(PermissionRequiredMixin, DeleteView):
    permission_required = ['profile.delete_profile']
    permission_denied_message = "You dont have permission to delete profile"
    raise_exception = True
    model = Profile

    def get_success_url(self):

        messages.success(self.request, 'Success, profile deleted', extra_tags='alert alert-info')

        return reverse_lazy('profile:home')


class UpdateProfile(PermissionRequiredMixin, FormView):
    template_name = 'accounts/edit_profile.html'
    permission_required = ['profile.change_profile']
    permission_denied_message = "You dont have permission to change profile"
    raise_exception = True
    form_class = UpdateProfileForm
    password_form = PasswordChangeForm

    def post(self, request, *args, **kwargs):

        person = get_object_or_404(Profile, pk=self.kwargs['pk'])

        form = self.form_class(instance=person, data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Success, profile details updated', extra_tags='alert alert-success')

            return redirect(to='profile:update-profile', pk=self.kwargs['pk'])
        else:

            context = {
                'form': self.form_class(data=request.POST, instance=person),
                'person': person,
                'password_form': self.password_form
            }

            messages.error(request, 'Failed, errors occurred.', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):

        person = get_object_or_404(Profile, pk=self.kwargs['pk'])

        password_form = self.password_form(user=person)

        password_form.fields['old_password'].widget.attrs.pop("autofocus", None)

        context = {
            'form': self.form_class(instance=person),
            'person': person,
            'password_form': password_form
        }

        return render(request, self.template_name, context=context)


class CreateProfile(PermissionRequiredMixin, FormView):
    template_name = 'accounts/create_profile.html'
    permission_required = ['profile.add_profile']
    permission_denied_message = "You dont have permission to add profile"
    form_class = CreateProfileForm

    def get(self, request, *args, **kwargs):

        profile = Profile.objects.all().order_by('-pk')[:10]
        persons = []

        if profile.count() > 0:

            num = 0

            for person in profile:

                num += 1

                persons.append({
                    'num': num,
                    'name': person.get_full_name(),
                    'email': person.email,
                    'phone_number': person.phone_number,
                    'pk': person.pk
                })

        context = {
            'form': self.form_class,
            'profile': persons
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            profile_obj = form.save(commit=False)
            profile_obj.is_profile = True

            # Set default password to phone_number
            profile_obj.set_password(
                raw_password=form.cleaned_data['phone_number']
            )

            profile_obj.save()

            messages.success(request, 'Success, profile created', extra_tags='alert alert-success')

            return redirect(to='profile:home')

        profiles = Profile.objects.all().order_by('-pk')[:10]
        persons = []

        if profiles.count() > 0:

            num = 0

            for person in profiles:
                num += 1

                persons.append({
                    'num': num,
                    'name': person.get_full_name(),
                    'email': person.email,
                    'phone_number': person.phone_number,
                    'pk': person.pk
                })

        context = {
            'form': form,
            'profiles': persons
        }

        messages.error(request, 'Errors occurred', extra_tags='alert alert-danger')

        return render(request, self.template_name, context=context)


class Logout(FormView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):

        logout(request)

        return redirect(to='/')


class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):

        if request.GET.get('next'):
            next_url = request.GET.get('next', '/profile/')
        else:
            next_url = '/profile/'

        context = {
            'next': next_url,
            'form': self.form_class
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        username = ''
        password = 'pa'

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = '/'

            return redirect(to=next_url)

        else:

            messages.error(request, 'Wrong username/password', extra_tags='alert alert-danger')

            form = self.form_class(initial={'username': username})

            return render(request, self.template_name, {'form': form})


class Home(PermissionRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'
    permission_required = ['profile.view_profile']
    permission_denied_message = "You dont have permission to view profile"
    raise_exception = True

    def get(self, request, *args, **kwargs):

        existing_profile = Profile.objects.all().order_by('-pk')
        profiles = []
        profile = None

        if existing_profile.count() > 0:

            num = 0

            for person in existing_profile:
                num = num + 1
                profiles.append({
                    'num': num,
                    'name': person.get_full_name(),
                    'phone_number': person.phone_number,
                    'email': person.email,
                    'pk': person.pk,
                })

        context = {
            'profile': profile
        }

        return render(request, self.template_name, context=context)


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            profile = form.save(commit=False)
            profile.is_active = False
            profile.save()

            mail_subject = 'Activate your user account.'
            message = render_to_string('accounts/template_activate_account.html', {
                'user': profile.last_name,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
                'token': account_activation_token.make_token(profile),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[profile.email])
            if email.send():
                messages.success(request, mark_safe(f'Please go to your email <b>{profile.email}</b> inbox and click on \
                        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'),
                                 extra_tags="alert alert-success")
            else:
                messages.error(request,
                               mark_safe(f'Problem sending confirmation email to <b>{profile.email}</b>, check if you typed it correctly.'),
                               extra_tags="alert alert-danger")

            return render(request, template_name=self.template_name)

        else:
            messages.error(request, 'Errors occurred in the form', extra_tags='alert alert-danger')

            return render(request, template_name=self.template_name, context={"form": form})


class ActivateAccount(TemplateView):
    model = Profile

    def get(self, request, uidb64=None, *args, **kwargs):

        token = kwargs["token"]
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            profile = self.model.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
            profile = None

        if profile is not None and account_activation_token.check_token(profile, token):
            profile.is_active = True
            profile.email_verified = True
            profile.save()

            messages.success(request,
                             'Email confirmed. Now you can login',
                             extra_tags="alert alert-success")

            return redirect('profiles:login')
        else:
            messages.error(request, 'Activation link is invalid!', extra_tags="alert alert-danger")

        return redirect('profiles:login')


class RequestPasswordChange(FormView):
    model = Profile
    template_name = 'accounts/request_password_change.html'
    form_class = RequestPasswordResetForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            try:
                profile = self.model.objects.get(email=form.cleaned_data['email'])
            except ObjectDoesNotExist:
                profile = None
            if profile is None:
                messages.error(request, "Email does not exist here", extra_tags='alert alert-info')
            else:
                #create token
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user=profile)

                html_msg = "Someone made a request to reset your password."
                html_msg += "<p>If this was you, please"
                html_msg += f"<a href='http://{get_current_site(request).domain}/profiles/reset-requested-password?token={token}&email={profile.email}' target='_blank'>"
                html_msg += "click here</a>.</p> Otherwise, ignore this email but also report to officials.<p>NOTE: This link can be used only once.</a>"

                send_mail(
                    subject="Password reset",
                    message="",
                    html_message=html_msg,
                    recipient_list=[profile.email],
                    from_email=settings.FROM_MAIL
                )

                messages.success(request, "Check your email inbox", extra_tags='alert alert-info')
        else:
            messages.error(request, "Errors occurred, form is not valid", extra_tags='alert alert-danger')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)


class ChangeRequestedPassword(FormView):
    model = Profile
    form_class = ResetPasswordForm
    template_name = "accounts/reset_requested_password.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = get_object_or_404(self.model, email=self.request.GET.get('email'))
        return kwargs

    def post(self, request, *args, **kwargs):

        profile = get_object_or_404(self.model, email=self.request.GET.get('email'))

        form = self.form_class(
            user=profile,
            data=request.POST
        )
        if form.is_valid():

            profile.set_password(raw_password=form.cleaned_data['new_password2'])
            profile.save()
            messages.success(request, 'New password created, login again', extra_tags='alert alert-success')

            try:
                send_mail(
                    subject='Password Changed',
                    message='Your password has just been changed. \nIf you did not make this change, please report the issue immediately. ',
                    from_email=settings.FROM_MAIL,
                    recipient_list=[profile.email],
                    fail_silently=True
                )
            except Exception:
                pass

            return redirect(to='profiles:login')
        else:
            context = {
                'profile': profile,
                'form': form
            }
            messages.error(request, 'Errors occurred', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)

