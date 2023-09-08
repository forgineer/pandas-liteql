from setuptools import setup


setup(
    name='pandas-liteql',
    version='0.1.0',
    author='forgineer',
    description='',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://github.com/forgineer/pandas-liteql',
    license='MIT License',
    packages=['pandas_liteql'],
    install_requires=[
        'pandas >= 1.5.3',
        'sqlalchemy >= 1.4.16',
    ],
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
