from setuptools import setup, find_packages


setup(
    name="PeachyBot",
    version="0.1",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["discord.py", "sqlalchemy"],

    entry_points={
        "console_scripts": [
            "peachy = peachy.main:bootstrap",
            "peachy_import_users = scripts.import_users:import_users"
        ],
    },

    # metadata to display on PyPI
    author="Benjamin Hoving",
    author_email="benjamin.hoving@gmail.com",
    description="Peachy's Bot on Discord",
)
