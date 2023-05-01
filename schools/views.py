from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DeleteView, TemplateView, DetailView

from schools.forms import CreateSchoolForm, UpdateSchoolForm, UploadPicturesForm, ApproveSchoolForm
from schools.models import School, Photo


class SchoolDetails(DetailView):
    model = School
    template_name = "schools/details.html"

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        context['pictures'] = Photo.objects.filter(school_id=self.kwargs['pk'])

        return context


class UpdateSchool(LoginRequiredMixin, FormView):
    template_name = 'schools/edit.html'
    permission_required = ['schools.change_school']
    permission_denied_message = "You dont have permission to change schools"
    raise_exception = True
    form_class = UpdateSchoolForm

    def post(self, request, *args, **kwargs):

        school = get_object_or_404(School, pk=self.kwargs['pk'])

        form = self.form_class(instance=school, data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Success, school details updated', extra_tags='alert alert-success')

            return redirect(to='schools:update', pk=self.kwargs['pk'])
        else:

            context = {
                'form': self.form_class(data=request.POST, instance=school),
                'school': school,
            }

            messages.error(request, 'Failed, errors occurred.', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):

        school = get_object_or_404(School, pk=self.kwargs['pk'])

        context = {
            'form': self.form_class(instance=school),
            'school': school,
        }

        return render(request, self.template_name, context=context)


class ApproveSchool(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'schools/approve.html'
    permission_denied_message = "You dont have permission to approve schools"
    raise_exception = True
    form_class = ApproveSchoolForm

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):

        school = get_object_or_404(School, pk=self.kwargs['pk'])

        form = self.form_class(instance=school, data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Success, school status is updated', extra_tags='alert alert-success')

            return redirect(to='schools:update', pk=self.kwargs['pk'])
        else:
            context = {
                'form': self.form_class(data=request.POST, instance=school),
                'school': school,
            }

            messages.error(request, 'Failed, errors occurred.', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):

        school = get_object_or_404(School, pk=self.kwargs['pk'])

        context = {
            'form': self.form_class(instance=school),
            'school': school,
        }

        return render(request, self.template_name, context=context)


class UploadPictures(LoginRequiredMixin, FormView):
    template_name = 'schools/upload_pictures.html'
    form_class = UploadPicturesForm
    model = Photo

    def post(self, request, *args, **kwargs):

        form = self.form_class(
            files=request.FILES,
            data=request.POST
        )
        school = get_object_or_404(School, pk=self.kwargs['pk'])
        pictures = self.model.objects.filter(school_id=self.kwargs['pk'])

        if form.is_valid():

            photo = form.save(commit=False)

            photo.school = school
            photo.created_by = self.request.user

            photo.save()

            messages.success(request, 'Success, photo saved. Select more picture to upload', extra_tags='alert alert-success')

        else:  # Form is not valid

            messages.error(request, 'Errors occurred. Please try a gain', extra_tags='alert alert-danger')
            context = {
                'form': form,
                'school': school,
                'pictures': pictures,
            }
            return render(request, template_name=self.template_name, context=context)

        return redirect(to='schools:upload_pictures', pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):

        school = get_object_or_404(School, pk=self.kwargs['pk'])
        pictures = self.model.objects.filter(school_id=self.kwargs['pk'])
        context = {
            'form': self.form_class(),
            'school': school,
            'pictures': pictures,
        }

        return render(request, self.template_name, context=context)


class DeleteSchool(PermissionRequiredMixin, DeleteView):
    permission_required = ['school.delete_school']
    permission_denied_message = "You dont have permission to delete schools"
    raise_exception = True
    model = School

    def get_success_url(self):

        messages.success(self.request, 'Success, school has been deleted', extra_tags='alert alert-info')

        return reverse_lazy('schools:list')


class CreateSchool(LoginRequiredMixin, CreateView):
    model = School
    template_name = "schools/create.html"
    form_class = CreateSchoolForm

    def get(self, request, *args, **kwargs):

        schools = self.model.objects.all().order_by('-pk')[:10]
        schools_dto = []

        if schools.count() > 0:
            num = 0
            for school in schools:
                num += 1
                schools_dto.append({
                    'num': num,
                    'name': school.name,
                    'primary_email': school.primary_email,
                    'primary_phone': school.primary_phone,
                    'pk': school.pk
                })

        context = {
            'form': self.form_class,
            'schools': schools_dto
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            school_obj = form.save(commit=False)
            school_obj.created_by = request.user
            school_obj.save()

            messages.success(request, 'Success, school has been created', extra_tags='alert alert-success')

            return redirect(to='schools:upload_pictures', pk=school_obj.pk)

        schools = School.objects.all().order_by('-pk')[:10]
        schools_dto = []

        if schools.count() > 0:
            num = 0
            for school in schools:
                num += 1
                schools_dto.append({
                    'num': num,
                    'name': school.name,
                    'email': school.email,
                    'primary_phone': school.primary_phone,
                    'pk': school.pk
                })

        context = {
            'form': form,
            'schools': schools_dto
        }

        messages.error(request, 'Errors occurred', extra_tags='alert alert-danger')

        return render(request, self.template_name, context=context)


class ListSchools(TemplateView):
    template_name = 'schools/list.html'

    def get(self, request, *args, **kwargs):

        existing_schools = School.objects.all().order_by('-pk')
        schools_dto = []

        if existing_schools.count() > 0:
            num = 0
            for school in existing_schools:
                num = num + 1
                schools_dto.append({
                    'num': num,
                    'name': school.name,
                    'primary_phone': school.primary_phone,
                    'primary_email': school.primary_email,
                    'description': school.description,
                    'pk': school.pk,
                })
        else:
            schools_dto = None

        context = {
            'schools': schools_dto
        }

        return render(request, self.template_name, context=context)
