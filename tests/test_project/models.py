from datetime import datetime

from django.db import models

from beproud.django.basemodels import (
    base,
    fields,
)


class DummyDatedModel(base.DatedModel):

    class Meta:
        app_label = 'test_project'


class DummyDatedModelManagerModel(models.Model):
    utime = models.DateTimeField()

    objects = base.DatedModelManager()

    def __str__(self):
        return ' '.join([
            'utime="{utime:%Y-%m-%d %H:%M:%S}"'
        ]).format(utime=self.utime)

    class Meta:
        app_label = 'test_project'


class DummyBaseManagerModel(models.Model):
    del_flg = models.BooleanField(default=False)
    utime = models.DateTimeField(default=datetime.now)

    objects = base.BaseManager()

    class Meta:
        app_label = 'test_project'


class DummyBaseModel(base.BaseModel):
    class Meta:
        app_label = 'test_project'


class DummyBigAutoFieldModel(models.Model):
    f = fields.BigAutoField(primary_key=True)

    class Meta:
        app_label = 'test_project'


class DummyNonIntegerPKModel(models.Model):
    id = models.CharField(primary_key=True, max_length=1)

    class Meta:
        app_label = 'test_project'


class DummyChildModel(models.Model):
    auto = models.ForeignKey(DummyBaseModel)
    big_auto = models.ForeignKey(DummyBigAutoFieldModel)
    non_int = models.ForeignKey(DummyNonIntegerPKModel)

    class Meta:
        app_label = 'test_project'
