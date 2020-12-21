from setuptools import setup, find_packages

# https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications

setup(
    name="audiobook-for-grandma",
    version="0.1",

    description='''A Raspberry Pi project for my blind grandmother, so that she can have an easy access to audiobooks online.''',

    author='Julien Perrin',
    author_email='julien.perrin25@gmail.com',

    url='https://github.com/JulienPerrin/audiobook-for-grandma',

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ),


    packages=find_packages(exclude=['test*', 'Test*']),

    package_data={
        '': ['README.md', 'LICENSE'],
        'audiobook-for-grandma': ['config.yaml']
      },

    licence='MIT License',

    scripts=['main.py'],

    entry_points={
          'console_scripts': [
              'audiobook-for-grandma = main:main',
          ],
      },

    install_requires=[
        'PyYAML==4.2b1',
        'gTTS==2.2.1',
      ],


)
