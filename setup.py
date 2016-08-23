from setuptools import setup, find_packages

setup(
    name = "geojson_utils",
    version = "0.0.1",
    description = "Python helper functions for manipulating GeoJSON",
    long_description = open('README.md').read(),
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    keywords = "python geojson util calculation",
    author = "brandonxiang",
    author_email = "1542453460@qq.com",
    url = "https://github.com/brandonxiang/geojson-python-utils",
    license = "MIT",
    install_requires=[
        'requests>=2.9.1',
    ],
    include_package_data = True,
    zip_safe = True
)