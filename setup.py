from distutils.core import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name='corebot',
    version='0.1',
    license="",
    description='Powerful platform agnostic chat bot',
    long_description=long_description,
    author='Chad Bailey',
    url='https://github.com/ChadBailey/hordesman',
    packages=['corebot'],
    install_requires=[
        'python-dotenv',
        'discord.py'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Chat',
        'Topic :: Text Processing :: Linguistic'
    ]
)