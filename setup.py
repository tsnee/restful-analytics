from setuptools import find_packages, setup

setup(
    name='restful-analytics',
    version='0.1.0',
    packages=['restful_analytics'],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'flask-restplus',
        'numpy',
    ],
)
