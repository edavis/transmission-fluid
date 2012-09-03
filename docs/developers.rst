Developers
==========

transmission-fluid is available on `Github
<https://github.com/edavis/transmission-fluid>`_ and welcomes
contributions.

Tests and Docs
--------------

transmission-fluid tries to uphold the Python ecosystem's commitment
to well-tested and well-documented code.

As such, use `tox <http://tox.testrun.org>`_ to run the full test
suite with different Python versions.

Contributions that include tests and docs will likely get acted upon
sooner than contributions that don't.

That said, if you have a bugfix or new feature for transmission-fluid but
aren't sure how to test it, just explain what you're trying to
do. We'll try to work something out. Same goes if English isn't your
first language -- just do what you can and we'll go from there.

.. image:: https://secure.travis-ci.org/edavis/transmission-fluid.png
   :target: http://travis-ci.org/#!/edavis/transmission-fluid

License
-------

MIT

Philosophy
----------

The goal of transmission-fluid is to be a thin wrapper around
Transmission's `RPC specification`_. It purposefully exposes most of
the RPC specification for the following reasons:

**Easy for developers**
   Once you've grasped Transmission's RPC specification, you can begin
   using transmission-fluid immediately. Just plug in a method name and any
   applicable request arguments and you're ready to go.

**Stays current**
   As the Transmission developers add more methods and arguments,
   you'll be able to use them right away instead of waiting for this
   wrapper to be updated to take advantage of them.

.. _RPC specification: https://trac.transmissionbt.com/browser/trunk/extras/rpc-spec.txt

