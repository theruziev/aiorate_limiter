.. image:: https://img.shields.io/travis/com/theruziev/rate_limiter.svg?style=flat-square
        :target: https://travis-ci.com/theruziev/rate_limiter
.. image:: https://img.shields.io/codecov/c/github/theruziev/rate_limiter.svg?style=flat-square
        :target: https://codecov.io/gh/theruziev/rate_limiter


Rate Limiter
============

A simple **asyncio** ready python implementation of a general purpose rate limiter based on
`Token Bucket algorithm <https://en.wikipedia.org/wiki/Token_bucket>`_.

Supported backends
--------------------
* Memory
* Redis (`aioredis <https://github.com/aio-libs/aioredis>_`)
* TODO: Memcached(`aiomcache <https://github.com/aio-libs/aiomcache>_`)
* TODO: PostgreSQL (`aiopg <https://github.com/aio-libs/aiopg>_`, `asyncpg <https://github.com/MagicStack/asyncpg>_`)
* TODO: MongoDB (`motor <https://github.com/mongodb/motor>_`)


Installation
------------

Install with the following command


```bash
pip install aiorate_limiter
```


Quickstart
----------

RateLimiter is really easy to use.  First of all you are need chose bucket type. If your app run only in one process, you can use MemoryBucket otherwise I advice to you use RedisBucket, it's fast, work with several instance. After one you need set bucket to RateLimiter and limit 


```python
from aiorate_limiter import RateLimiter
from aiorate_limiter.buckets import MemoryBucket
import asyncio

loop = asyncio.get_event_loop()

mail = Mail()

loop.run_until_complete(mail.send_message("Hello", from_address="from@example.com",
                  to="to@example.com", body="Hello world!"))
```



