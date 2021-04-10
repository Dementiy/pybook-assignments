from setuptools import setup

setup(
    name="httpserver",
    version="0.0.1",
    packages=["httpserver"],
    install_requires=[
        "httptools",
        'importlib; python_version >= "3.6"',
    ],
)
