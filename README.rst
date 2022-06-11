selfcord.py-self
================

.. image:: https://img.shields.io/endpoint?url=https%3A%2F%2Frunkit.io%2Fdamiankrawczyk%2Ftelegram-badge%2Fbranches%2Fmaster%3Furl%3Dhttps%3A%2F%2Ft.me%2Fdpy_self
   :target: https://t.me/dpy_self
   :alt: Telegram chat
.. image:: https://img.shields.io/pypi/v/selfcord.py-self.svg
   :target: https://pypi.python.org/pypi/selfcord.py-self
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/selfcord.py.svg
   :target: https://pypi.python.org/pypi/selfcord.py-self
   :alt: PyPI supported Python versions
.. image:: https://img.shields.io/pypi/dm/selfcord.py-self.svg
   :target: https://pypi.python.org/pypi/selfcord.py-self
   :alt: PyPI downloads per month

A modern, easy to use, feature-rich, and async ready API wrapper for Discord's user API written in Python.

Fork Changes
------------

These changes have become too numerous to mention, so check out our `docs <https://selfcordpy-self.readthedocs.io/en/latest/index.html>`_.

| **Credits:**
| - `arandomnewaccount <https://www.reddit.com/user/obviouslymymain123/>`_ for Discord API help.
|

| **Note:**
| Automating user accounts is against the Discord ToS. This library is a proof of concept and I do not recommend using it. Do so at your own risk.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.
- Mostly compatible with the official ``selfcord.py``.
- Prevents selfbot detection.

Installing
----------

**Python 3.8 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U selfcord.py-self

    # Windows
    py -3 -m pip install -U selfcord.py-self

Otherwise to get voice support you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "selfcord.py-self[voice]"

    # Windows
    py -3 -m pip install -U selfcord.py-self[voice]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/dolfies/selfcord.py-self
    $ cd selfcord.py-self
    $ python3 -m pip install -U .[voice]


Optional Packages
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (for voice support)

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)

Quick Example
--------------

.. code:: py

    import selfcord

    class MyClient(selfcord.Client):
        async def on_ready(self):
            print('Logged on as', self.user)

        async def on_message(self, message):
            # only respond to ourselves
            if message.author != self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

    client = MyClient()
    client.run('token')

Bot Example
~~~~~~~~~~~~~

.. code:: py

    import selfcord
    from selfcord.ext import commands

    bot = commands.Bot(command_prefix='>', self_bot=True)

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    bot.run('token')

You can find more examples in the examples directory.

Links
------

- `Documentation <https://selfcordpy-self.readthedocs.io/en/latest/index.html>`_
- `Project updates <https://t.me/dpy_self>`_
- `Discussion & support <https://t.me/dpy_self_discussions>`_
