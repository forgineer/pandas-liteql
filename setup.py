from setuptools import setup


# Use README file as long description
with open("README.md") as f:
    long_description = f.read()


setup(
    name='pandas-liteql',
    version='0.3.6',
    author='forgineer',
    description="""An extension for pandas, enabling users to execute SQL statements on pandas DataFrames, 
    streamlining data manipulation and analysis tasks""",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/forgineer/pandas-liteql',
    license='MIT License',
    packages=['pandas_liteql'],
    python_requires='>=3.7',
    install_requires=[
        'pandas >= 1.3.5',
        'sqlalchemy >= 1.4.36',
    ],
    extras_require={  # pip install -e .[dev]
        'dev': [
            'build',
            'twine'
        ]
    },
    keywords='dataframe,pandas,sql,sqlite',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)

"""
Build and deploy steps:
    - python -m build
    - twine check dist/*
    - twine upload -r testpypi dist/*
    - twine upload dist/*
"""
