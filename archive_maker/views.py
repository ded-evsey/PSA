from django.utils import timezone
from django.conf import settings
from django.views.generic import TemplateView, FormView
from .forms import ArchiveForm
from .models import ArchiveIP
# Create your views here.


class Homepage(TemplateView):
    template_name = 'base.html'


class ArchivesView(FormView):
    form_class = ArchiveForm
    template_name = 'arhive_maker/archives.html'
    success_url = 'archives'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archives = ArchiveIP.objects.filter(
            ip=self.request.META.get('REMOTE_ADDR')
        )
        context['files'] = archives
        context['disabled'] = not archives.filter(
            uploaded_at=timezone.now().date()
        ).count() <= settings.MAX_FILES_PER_DAY
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        ArchiveIP.make_archive(
            self.request.FILES.getlist('files'),
            self.request.META.get('REMOTE_ADDR'),
            data.get('extension'),
            data.get('filename')
        )
        return super().form_valid(form)
