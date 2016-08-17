import pytest
import mock


@pytest.mark.django_db
class TestBigAutoField(object):
    @pytest.fixture
    def model_cls(self):
        from test_project.models import DummyBigAutoFieldModel
        return DummyBigAutoFieldModel

    @pytest.fixture
    def target(self):
        from beproud.django.basemodels.fields import BigAutoField
        return BigAutoField

    @pytest.fixture
    def connection_proxy(self):
        from django.db import DefaultConnectionProxy
        return mock.Mock(spec=DefaultConnectionProxy)

    @pytest.fixture
    def database_wrapper_cls(self):
        class DatabaseWrapper(object):
            def __init__(self):
                self.settings_dict = {
                    'ENGINE': 'test_engine'
                }

        return DatabaseWrapper

    @pytest.fixture
    def database_wrapper(self, database_wrapper_cls):
        return database_wrapper_cls()

    @pytest.fixture
    def backend(self, database_wrapper_cls):
        class Module(object):
            def __init__(self):
                self.DatabaseWrapper = database_wrapper_cls

        return Module()

    @pytest.fixture
    def django_db_connections(self, database_wrapper_cls):
        from django.db.utils import DEFAULT_DB_ALIAS
        return {DEFAULT_DB_ALIAS: mock.Mock(spec=database_wrapper_cls)}

    @pytest.fixture
    def connection_factory(self, connection_proxy, database_wrapper):
        return lambda type_: {
            'connection_proxy': connection_proxy,
            'database_wrapper': database_wrapper,
        }.get(type_)

    @pytest.fixture
    def exception_factory(self):
        from django.core import exceptions
        return lambda type_: {
            'ImportError': ImportError,
            'ImproperlyConfigured': exceptions.ImproperlyConfigured,
            'KeyError': KeyError,
            'AttributeError': AttributeError,
        }.get(type_)

    @pytest.mark.parametrize(
        'connection_type',
        (
            'connection_proxy',
            'database_wrapper',
        )
    )
    def test_db_type(
            self,
            target, backend, connection_factory, django_db_connections,
            connection_type
    ):
        # arrange
        field = target()
        field.CREATION_DATA = {'path.to.module': 'test_db_type'}
        connection = connection_factory(connection_type)

        # act
        with mock.patch(
                'beproud.django.basemodels.fields.load_backend',
                return_value=backend,
        ):
            with mock.patch('django.db.connections', django_db_connections):
                actual = field.db_type(connection)

        # assert
        assert actual == 'test_db_type'

    @pytest.mark.parametrize(
        'exception',
        (
            'ImportError',
            'ImproperlyConfigured',
            'KeyError',
            'AttributeError',
        )
    )
    def test_db_type_raise(
            self,
            target, backend, database_wrapper, exception_factory,
            exception,
    ):
        # arrange
        from django.core import exceptions
        field = target()
        field.CREATION_DATA = {'path.to.module': 'test_db_type'}
        exception_cls = exception_factory(exception)

        # act
        with mock.patch(
                'beproud.django.basemodels.fields.load_backend',
                side_effect=exception_cls,
        ):
            with pytest.raises(exceptions.ImproperlyConfigured):
                field.db_type(database_wrapper)

    @pytest.mark.parametrize(
        'value,expected',
        (
            (None, None),
            (1, long(1)),
        )
    )
    def test_get_prep_value(self, target, value, expected):
        # arrange
        field = target()

        # act
        actual = field.get_prep_value(value)

        # assert
        assert actual == expected

    @pytest.mark.parametrize(
        'value,expected',
        (
            (None, None),
            ('1', long(1)),
        )
    )
    def test_to_python(self, target, value, expected):
        # arrange
        field = target()

        # act
        actual = field.to_python(value)

        # assert
        assert actual == expected

    def test_to_python_raises(self, target):
        # arrange
        from django.core.exceptions import ValidationError
        field = target()

        # act/assert
        with pytest.raises(ValidationError):
            field.to_python(object())

    def test_it(self, model_cls):
        # act
        model_cls.objects.create()
        model_cls.objects.create()
        model_cls.objects.create()
        actual = model_cls.objects.order_by('f')

        # assert
        assert [1, 2, 3] == [m.f for m in actual]


@pytest.mark.django_db
class TestPositiveBigIntegerField(object):
    @pytest.fixture
    def target(self):
        from beproud.django.basemodels.fields import PositiveBigIntegerField
        return PositiveBigIntegerField

    def test_it(self, target):
        from django.core.exceptions import ValidationError
        formfield = target().formfield()

        with pytest.raises(ValidationError):
            formfield.clean(-1)

        formfield.clean(0)
        formfield.clean(1)


@pytest.mark.django_db
class TestPickledObjectField(object):
    @pytest.fixture
    def target(self):
        from beproud.django.basemodels.fields import PickledObjectField
        return PickledObjectField

    @pytest.fixture
    def model_cls(self):
        from test_project.models import DummyPickleFieldModel
        return DummyPickleFieldModel

    def test_it(self, model_cls):
        # setup
        object_ = {'a': [1, 2, 3], 'b': ('AAA', 'BBB'), 'c': None}

        # act
        instance = model_cls.objects.create(
            pickled_object=object_,
        )
        gotten = model_cls.objects.get(pk=instance.pk)

        # assert
        assert gotten.pickled_object == object_

    @pytest.mark.parametrize(
        'value,expected',
        (
            (None, None),
            ('aaa', 'UydhYWEnCnAxCi4='),
        )
    )
    def test_get_db_prep_save(self, value, expected, target):
        # arrange
        field = target()

        # act
        actual = field.get_db_prep_save(value)

        # assert
        assert actual == expected

    @pytest.mark.parametrize(
        'value,expected',
        (
            (None, None),
            ('UydhYWEnCnAxCi4=', 'aaa'),
        )
    )
    def test_from_db_value(self, value, expected, target):
        # arrange
        field = target()

        # act
        actual = field.from_db_value(value, None, None, None)

        # assert
        assert actual == expected


@pytest.mark.django_db
class TestFkDbType(object):
    @pytest.fixture
    def auto_pk_model(self):
        from test_project.models import DummyBaseModel
        return DummyBaseModel

    @pytest.fixture
    def big_auto_pk_model(self):
        from test_project.models import DummyBigAutoFieldModel
        return DummyBigAutoFieldModel

    @pytest.fixture
    def non_inteter_pk_model(self):
        from test_project.models import DummyNonIntegerPKModel
        return DummyNonIntegerPKModel

    @pytest.fixture
    def child_cls(self):
        from test_project.models import DummyChildModel
        return DummyChildModel

    def test_it(
            self,
            child_cls, auto_pk_model, big_auto_pk_model, non_inteter_pk_model,
    ):
        # setup
        auto_1 = auto_pk_model.objects.create()
        auto_2 = auto_pk_model.objects.create()
        big_auto_1 = big_auto_pk_model.objects.create()
        big_auto_2 = big_auto_pk_model.objects.create()
        non_int_1 = non_inteter_pk_model.objects.create(id='a')
        non_int_2 = non_inteter_pk_model.objects.create(id='b')

        # create
        child = child_cls.objects.create(
            auto=auto_1,
            big_auto=big_auto_1,
            non_int=non_int_1,
        )

        # read
        actual_read = child_cls.objects.all()
        expected = [{
            'auto': auto_1,
            'big_auto_1': big_auto_1,
            'non_int_1': non_int_1,
        }]
        assert expected == [{
            'auto': m.auto,
            'big_auto_1': m.big_auto,
            'non_int_1': m.non_int,
        } for m in actual_read]

        # update
        child.auto = auto_2
        child.big_auto = big_auto_2
        child.non_inta = non_int_2
        child.save()

        # delete
        child.delete()
        actual_deleted = child_cls.objects.all()
        assert list(actual_deleted) == []  # QueryDict -> List
