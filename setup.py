from setuptools import find_packages, setup

# https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications

setup(
    name="audiobook-for-grandma",
    version="0.21",
    description="""A Raspberry Pi project for my blind grandmother, so that she can have an easy access to audiobooks online.""",
    author="Julien Perrin",
    author_email="julien.perrin25@gmail.com",
    url="https://github.com/JulienPerrin/audiobook-for-grandma",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["test*", "Test*"]),
    include_package_data=True,
    license="MIT",
    scripts=["main.py"],
    entry_points={
        "console_scripts": [
            "audiobook-for-grandma = main:main",
        ],
    },
    install_requires=[
        "PyYAML",
        "pytest",
        "internetarchive",
        "pyttsx3",
        "chardet",
        "EbookLib",
        "bs4",
        "setuptools",
        "build",
    ],
)
