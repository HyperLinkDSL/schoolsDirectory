from django.shortcuts import render
from django.views.generic import TemplateView

from schools.models import School


class Home(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        schools = School.objects.all().order_by('-pk')[:10]

        context = {
            "recent_schools": schools
        }

        return render(request, template_name=self.template_name, context=context)


class About(TemplateView):
    template_name = "about.html"
