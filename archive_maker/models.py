import patoolib
import shutil
import os
from django.core.files import File
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import FileExtensionValidator
# Create your models here.


def get_upload_to(instance, filename):
    return 'archives/%s/%s' % (instance.ip, os.path.basename(filename))


class ArchiveIP(models.Model):
    archive = models.FileField(
        'Архив',
        upload_to=get_upload_to,
        validators=[FileExtensionValidator(
            allowed_extensions=settings.ARCHIVE_EXTENSION
        )]
    )
    ip = models.GenericIPAddressField()
    uploaded_at = models.DateField(
        'Дата загрузки',
        default=timezone.now().date()
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return os.path.basename(self.archive.name)

    @classmethod
    def make_archive(cls, files, ip, ext, filename):
        total_files_count = cls.objects.filter(
            uploaded_at=timezone.now().date(),
            ip=ip
        ).count()
        if settings.MAX_FILES_PER_DAY <= total_files_count:
            return
        media_temp_dir = os.path.join(
            settings.MEDIA_ROOT, 'temp_dir'
        )
        archive_dir = os.path.join(
            media_temp_dir,
            filename + '.' + ext
        )
        if not os.path.exists(media_temp_dir):
            os.mkdir(media_temp_dir,)
        temp_files = []
        for f in files:
            with open(
                    os.path.join(
                        media_temp_dir, f.name
                    ),
                    'wb'
            ) as file:
                file.write(f.file.getvalue())
                temp_files.append(file.name)
        patoolib.create_archive(
            archive_dir,
            temp_files
        )

        cls.objects.create(
            archive=File(open(archive_dir, 'rb')),
            ip=ip,
        )

        shutil.rmtree(media_temp_dir)
        return



