try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """
transmission-fluid is a Python wrapper for Transmission's RPC interface.

.. image:: https://secure.travis-ci.org/edavis/transmission-fluid.png
   :target: http://travis-ci.org/#!/edavis/transmission-fluid

::

    >>> from transmission import Transmission
    >>> client = Transmission()
    >>> client('torrent-get', ids=range(1,11), fields=['name'])
    {u'torrents': [
      {u'name': u'Elvis spotted in Florida.mov'},
      {u'name': u'Bigfoot sings the hits'},
      # ...
      {u'name': u'a-song-of-ice-and-fire_final-chapter.txt'}
    ]}

See the `README <https://github.com/edavis/transmission-fluid#readme>`_ for more information.
"""

setup(
    name = "transmission-fluid",
    version = "0.4",
    description = "A Python wrapper for Transmission's RPC interface",
    long_description = long_description,
    author = "Eric Davis",
    author_email = "ed@npri.org",
    url = "https://github.com/edavis/transmission-fluid",
    download_url = "http://pypi.python.org/pypi/transmission-fluid",
    packages = ["transmission"],
    install_requires = ["requests>=1.2.3"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
    ]
)
