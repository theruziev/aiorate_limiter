.. image:: https://img.shields.io/travis/com/theruziev/aiorate_limiter.svg?style=flat-square
        :target: https://travis-ci.com/theruziev/aiorate_limiter
.. image:: https://img.shields.io/codecov/c/github/theruziev/aiorate_limiter.svg?style=flat-square
        :target: https://codecov.io/gh/theruziev/aiorate_limiter


AioRate Limiter
===============

A simple **asyncio**-ready Python implementation of a general purpose rate limiter based on
`Token Bucket algorithm <https://en.wikipedia.org/wiki/Token_bucket>`_.

Supported storage
-----------------

* Memory
* Redis (`aioredis <https://github.com/aio-libs/aioredis>`_)


⚡ Quickstart
-------------

RateLimiter is really easy to use.

Basic Example:
~~~~~~~~~~~~~~

.. code-block:: python

	# 5 req/sec
	opts = RateLimiterOpts(points=5, duration=1000)
	limiter = MemoryRateLimiter(opts)
	# initialize limiter
	await limiter.init()
	# Consume
	result = limiter.consume("request_1", 1) # Consume for a request_1 1 point
	# Check is allowed
	if result.is_allowed:
		# Happy!!! 1 point consumed
	else:
		# Be a strong, points is ended. Try again later.


RateLimiterOpts
~~~~~~~~~~~~~~~

Options class for a configure rate limiter

**Params:**

* **points** - Maximum number of points can be consumed over duration
* **duration** - Number of milliseconds before consumed points are reset
* **key_prefix** - If you need to create several limiters for different purpose.


RateLimiterResult
~~~~~~~~~~~~~~~~~

An object which returned when consume points

**Params:**

* **remaining_points** - Number of remaining points in current duration
* **ms_before_next** - Number of milliseconds before next action can be done
* **consumed_points** - Number of consumed points in current duration
* **is_allowed** - Result of consume, true if allow otherwise false


Developing
-------------

To install development dependencies:

.. code-block:: bash

    make install

Lint:

.. code-block:: bash

    make lint


Formatting code:

.. code-block:: bash

    make format

Test:

.. code-block:: bash

    make test
    # or run tox
    tox

