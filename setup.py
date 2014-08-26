from setuptools import setup

with open('README.rst') as f:                                                                   
    long_description = f.read()

setup(
    name="gfwlist2pac",
    version="1.0.7",
    license='MIT',
    description="convert gfwlist2pac to pac",
    author='clowwindy',
    author_email='clowwindy42@gmail.com',
    url='https://github.com/clowwindy/gfwlist2pac',
    packages=['gfwlist2pac', 'gfwlist2pac.resources'],
    package_data={
        'gfwlist2pac': ['README.rst', 'LICENSE', 'resources/*']
    },
    install_requires=[],
    entry_points="""
    [console_scripts]
    gfwlist2pac = gfwlist2pac.main:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    long_description=long_description,
)
