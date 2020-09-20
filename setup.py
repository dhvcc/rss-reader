from setuptools import setup, find_packages
import os


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


with open("rss_reader/__init__.py") as f:
    """Executing init to set __version__ value"""
    exec(f.read())

setup(
    name="rss-reader",
    version=locals()["__version__"],
    author="dhvcc",
    author_email="1337kwiz@gmail.com",
    description="A simple CLI rss reader",
    url="https://github.com/dhvcc/rss-reader",
    license="MIT",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["requests",
                      "pydantic",
                      "bs4",
                      "colorama",
                      "Jinja2",
                      "ebooklib"],
    extras_require={
        "speedups": [
            "ujson"
        ],
        "dev": [
            "pre-commit",
            "autoflake",
            "autopep8",
            "pytest",
            "flake8"
        ]
    },
    include_package_data=True,
    keywords="python cli rss reader parser",
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        "console_scripts":
            ["rss-reader=rss_reader.__main__:main"],
    }
)
