import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gecko",
    version="0.0.1",   
    author="Artem Krasnyi",
    author_email='artkrasnyy@gmail.com',
    description="Utility lib for the Sungrazer project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=["gecko"],
    package_dir={'':'src/gecko'},
    install_requires=[
        "numpy>=1.24.0",
        "Pillow>=10.1.0",
        "ipython>=8.12.0",
        "ipython-genutils>=0.2.0",
    ]
)