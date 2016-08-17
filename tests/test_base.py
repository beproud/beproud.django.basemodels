from datetime import datetime

import pytest


@pytest.mark.django_db
class TestDatedModel(object):
    @pytest.fixture
    def model_cls(self):
        from test_project.models import DummyDatedModel
        return DummyDatedModel

    def test_ctime(self, model_cls):
        # arrange
        before = datetime.now()

        # act
        actual = model_cls.objects.create()

        # assert
        assert before < actual.ctime < datetime.now()

    def test_utime(self, model_cls):
        # arrange
        before = datetime.now()
        model_obj = model_cls.objects.create()

        # act
        model_obj.save()

        # assert
        assert before < model_obj.utime < datetime.now()
        assert model_obj.ctime < model_obj.utime


@pytest.mark.django_db
class TestDatedModelManager(object):
    @pytest.fixture
    def model_cls(self):
        from test_project.models import DummyDatedModelManagerModel
        return DummyDatedModelManagerModel

    def test_recently_updated(self, model_cls):
        # arrange
        models = [
            model_cls.objects.create(utime=datetime(2016, 1, 1, 0, 0, 1)),
            model_cls.objects.create(utime=datetime(2016, 1, 1, 0, 0, 2)),
            model_cls.objects.create(utime=datetime(2016, 1, 1, 0, 0, 3)),
        ]

        # act
        actual = model_cls.objects.recently_updated()

        # assert
        assert list(actual) == list(reversed(models))  # QuerySet -> List


@pytest.mark.django_db
class TestBaseModel(TestDatedModel):
    @pytest.fixture
    def model_cls(self):
        from test_project.models import DummyBaseModel
        return DummyBaseModel

    def test_remove(self, model_cls):
        # arrange
        model_obj = model_cls.objects.create()

        # act
        model_obj.remove()
        actual = model_cls.objects.get(pk=model_obj.pk)

        # assert
        assert actual.del_flg

    def test_unremove(self, model_cls):
        # arrange
        model_obj = model_cls.objects.create(del_flg=True)

        # act
        model_obj.unremove()
        actual = model_cls.objects.get(pk=model_obj.pk)

        # assert
        assert not actual.del_flg


@pytest.mark.django_db
class TestBaseManager(TestDatedModelManager):
    @pytest.fixture
    def model_cls(self):
        from test_project.models import DummyBaseManagerModel
        return DummyBaseManagerModel

    def test_be(self, model_cls):
        # arrange
        model_cls.objects.create(del_flg=True)
        remains = [
            model_cls.objects.create(del_flg=False),
            model_cls.objects.create(del_flg=False),
        ]

        # act
        actual = model_cls.objects.be()

        # assert
        assert list(actual) == remains  # QuerySet -> List
