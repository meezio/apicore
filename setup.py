from setuptools import setup

setup(
    name='apicore',
    version=1.0,
    packages=['apicore'],
    author="Meezio SAS",
    author_email="dev@meez.io",
    description="Core lib for REST API",
    # long_description=open('README.md').read(),
    # Active la prise en compte du fichier MANIFEST.in
    # include_package_data=True,
    url='https://github.com/meezio/apicore',
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        "Topic :: Software Development :: Libraries"
    ],
    license="MIT",
    install_requires=[
        'termcolor',
        'Flask',
        'PyYAML',
        'python-jose',
        'redis'
    ]
)
