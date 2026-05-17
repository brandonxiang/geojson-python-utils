from setuptools import setup, find_packages

setup(
    name = "geojson_utils",
    version = "0.0.1",
    description = "Python helper functions for manipulating GeoJSON",
    long_description = open('README.md').read(),
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        "geojson_utils": ["py.typed"],
    },
    python_requires=">=3.8",
    keywords = "python geojson util calculation",
    author = "brandonxiang",
    author_email = "1542453460@qq.com",
    url = "https://github.com/brandonxiang/geojson-python-utils",
    license = "MIT",
    install_requires=[
        'requests>=2.9.1',
    ],
    entry_points={
        "console_scripts": [
            "geojson-utils=geojson_utils.cli:main",
        ],
    },
    include_package_data = True,
    zip_safe = True
)
