import os
import setuptools

long_description = ''
if os.path.exists('README.md'):
    with open('README.md') as f:
        loag_description = f.read()


setuptools.setup(
    name='dotdict',
    version='1.0.0',
    author='Brandon Jaus',
    author_email='brandon.jaus@gmail.com',
    description='dict implementation with attribute access',
    long_description=long_description,
    log_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['tests']),
    tests_require=['pytest'],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ],
)
