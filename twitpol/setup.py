import setuptools


setuptools.setup(
    name='twitpol',
    version='0.0.1',
    author='Benjamin Levy, Dimitris Vamvourellis, Matthieu Meeus, Will Fried',
    author_email='benjaminlevy@g.harvard.edu',
    description='Functions and variables for predicting political opinion polls from Twitter data',
    url='https://github.com/benlevyx/twitter-polling',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
