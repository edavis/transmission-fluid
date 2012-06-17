from distutils.core import setup

setup(
    name = "transmission-fluid",
    version = "0.1",
    description = "A Python wrapper for Transmission's RPC interface",
    long_description = "See the README: https://github.com/edavis/transmission-fluid#readme",
    author = "Eric Davis",
    author_email = "ed@npri.org",
    url = "https://github.com/edavis/transmission-fluid",
    py_modules = ['transmission'],
    license = 'MIT',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
    ]
)
