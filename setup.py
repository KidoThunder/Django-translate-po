import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Django-translate_po",
    version="0.1.0",
    author="Kido Zhao",
    author_email="zgdisgod@hotmail.com",
    description="Automatic PO file translator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KidoThunder/translate-po",
    packages=setuptools.find_packages(exclude=['docs', 'tests']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Internationalization',
    ],
    python_requires='>=3.6',
    keywords='Django po translate automatic google & AWS',
    project_urls={
        'Source': 'https://github.com/KidoThunder/translate-po',
        'Documentation': 'https://github.com/KidoThunder/translate-po/docs/main.html',
        'Author': 'http://blog.zkido.cc',
    },
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    install_requires=[
        'polib>=1.1.0',
        'googletrans>=3.0.0',
        'django>=2.1.12',
        'boto3>=1.17.91',
        'redis>=3.5.3'
    ],
    setup_requires=[
        'polib>=1.1.0',
        'googletrans>=3.0.0',
        'django>=2.1.12',
        'boto3>=1.17.91',
        'redis>=3.5.3'
    ],
)
