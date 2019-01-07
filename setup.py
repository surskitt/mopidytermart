from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="mopidytermart",
    version='0.1',
    packages=['mopidytermart'],
    install_requires=[
        'ueberzug',
        'python-mpd2',
        'mopidyartfetch'
    ],
    entry_points={
        "console_scripts": ['mopidytermart = mopidytermart.mopidytermart:main']
        },
    description="Display mopidy album art in the terminal",
    long_description=readme(),
    author="Shane Donohoe",
    author_email="donohoe.shane@gmail.com",
    url="https://github.com/sharktamer/mopidytermart",
    )
