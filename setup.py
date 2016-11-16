from setuptools import setup, find_packages


requires = [
    'django>=1.8',
]

setup(
    name='beproud.django.basemodels',
    version='0.1.0',
    description='beproud.django.basemodels provides base models and fields, that comes from bpcommons.',
    author='BeProud Inc.',
    author_email='xiao@beproud.jp',
    url='http://www.beproud.jp/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    namespace_packages=[
        'beproud',
        'beproud.django',
    ],
    install_requires=requires,
    zip_safe=False,
)
