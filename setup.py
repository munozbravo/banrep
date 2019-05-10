from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as fh:
    long_one = fh.read()

setup(
    name="banrep",
    version="0.0.1",
    description="Funciones y rutinas para BanRep",
    long_description=long_one,
    long_description_content_type="text/markdown",
    url="https://github.com/munozbravo/banrep",
    author="Germán Muñoz",
    author_email="gamunozbravo@gmail.com",
    packages=find_packages(exclude=['docs', 'tests']),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=3.7',
    include_package_data=True,
    install_requires=[
        "spacy>=2.1.3",
        "tika>=1.19"
    ]
)
