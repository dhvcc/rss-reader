from setuptools import setup, find_packages
import os


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


pkg_info = {}

with open("rss_reader/__version__.py") as f:
    """Executing init to set __version__ value"""
    exec(f.read(), pkg_info)

REPO_URL = "https://github.com/dhvcc/rss-reader"
SITE_URL = "https://dhvcc.github.io/rss-reader"

setup(
    name="rss-reader",
    version=pkg_info["__version__"],
    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description="A simple CLI rss reader",
    url=REPO_URL,
    license=pkg_info["__license__"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "rss-parser",
        "pathvalidate",
        "requests",
        "pydantic",
        "bs4",
        "lxml",
        "weasyprint",
        "colorama",
        "Jinja2",
        "ebooklib"
    ],
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
    project_urls={
        "Homepage": SITE_URL,
        "Source": REPO_URL,
        "Documentation": f"{SITE_URL}#documentation",
        "Tracker": f"{REPO_URL}/issues",
    },
    keywords=[
        "python", "python3", "cli",
        "rss", "reader", "parser",
        "mit", "mit-license"
    ],
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
