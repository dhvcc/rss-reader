from setuptools import setup, find_packages
import os
from rss_reader.config import version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='rss-reader',
    version=version,
    author='Alexey Artishevskiy',
    author_email='1337kwiz@gmail.com',
    description='A simple CLI rss reader',
    url='https://github.com/Kwizchm/PythonHomework',
    license='MIT',
    long_description=read('README.rst'),
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['bs4',
                      'weasyprint',
                      'python-magic',
                      'yattag',
                      'ebooklib',
                      'colorama',
                      'requests'],
    keywords='cli rss reader',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts':
            ['rss-reader=rss_reader.__main__:main'],
    }
)
