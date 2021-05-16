from django import forms

from django.conf import settings


class ArchiveForm(forms.Form):
    files = forms.FileField(
        label='Файлы, которые будут добавленны в архив',
        widget=forms.ClearableFileInput(
            attrs={'multiple': True}
        )
    )
    filename = forms.CharField(
        label='Название для архива',
        max_length=12
    )
    extension = forms.ChoiceField(
        label='Расширение',
        choices=[
            (ext, ext)
            for ext in settings.ARCHIVE_EXTENSION
        ]
    )
