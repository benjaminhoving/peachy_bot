from setuptools import setup, find_packages


setup(
    name="PeachyBot",
    version="0.1",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["discord.py"],

    entry_points={
        "console_scripts": [
            "peachy = peachy.main:main",
        ],
    },

    # metadata to display on PyPI
    author="Benjamin Hoving",
    author_email="benjamin.hoving@gmail.com",
    description="Peachy's Bot on Discord",
)
