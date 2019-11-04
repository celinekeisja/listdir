import setuptools

setuptools.setup(
    name='listdir',
    version='1.0',
    description='A program that takes the path of a directory and lists the Parent Path, File Name, and File Size of the files within that directory into a database, json file, or csv file.',
    url='https://github.com/celinekeisja/listdir/tree/write-to-db',
    author='Celine Keisja Nebrija',
    author_email='celinekeisja_nebrija@trendmicro.com',
    license='MIT',
    packages=['listdir'],
    classifiers=[
        'Intended Audience :: Sir Anwar Sumawang',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    python_requires='>=3.7'
)