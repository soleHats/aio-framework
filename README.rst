aio-framework
=============

A Python website bot development framework (WIP)

Introduction
------------

This project was created to aid the development of website bots and API
wrappers. ``aio-framework`` handles task management and execution,
session management, and captcha queue management (with threads!).
Currently, captcha queue management supports 2Captcha. ``aio-framework``
is meant to decrease development time by providing common bot and API
wrapper functionality.

Basic Usage
-----------

This module is available via pip:

::

    $ pip install aio-framework

Basic ``ApiWrapper`` and ``Bot`` implementations are shown below.
``Bot`` implementations *must* implement the ``execute_task`` method.

ApiWrapper
~~~~~~~~~~

.. code:: python

    # exampleapiwrapper.py
    from aio import ApiWrapper

    class ExampleApiWrapper(ApiWrapper):
        BASE_URL = 'https://example.com'

        def get_product_data(self, product_url):
            response = self.get(product_url)
            return response.json()['data'] # Or something

        def add_product_to_cart(self, product_data, captcha_token):
            payload = {
                'product_data': product_data,
                'captcha': captcha_token
            }
            endpoint = '/add-to-cart'
            response = self.post(endpoint, data=payload)
            return response.json()['success'] # Or something

Bot
~~~

.. code:: python

    # examplebot.py
    from aio import Bot
    from aio.captcha import CaptchaManager
    from exampleapiwrapper import ExampleApiWrapper

    class ExampleBot(Bot):
        def execute_task(self, task):
            example_api_wrapper = ExampleApiWrapper()

            twocaptcha_api_token = '2CAPTCHA_API_TOKEN_HERE'
            site_key = 'SITE_KEY_HERE'
            page_url = 'PAGE_URL_HERE'

            captcha_manager = CaptchaManager(twocaptcha_api_token, site_key, page_url)
            captcha_manager.start_captcha_queue(num_threads=5)

            task.status = 'STARTED'

            product_url = task.data['product_url']

            task.logger.info('Getting product data')
            product_data = example_api_wrapper.get_product_data(product_url)
            task.logger.info('Got product data!')

            task.logger.info('Waiting for captcha token')
            captcha_token = captcha_manager.wait_for_captcha_token()
            task.logger.info('Got captcha token!')

            task.logger.info('Adding product to cart')
            added = example_api_wrapper.add_product_to_cart(product_data, captcha_token)
            task.logger.info('Added product to cart!')

            task.status = 'FINISHED'

Executing
~~~~~~~~~

.. code:: python

    # main.py
    from aio import Task
    from examplebot import ExampleBot

    example_bot = ExampleBot()
    task_data = {
        'product_url': 'https://example.com/product'
    }
    task = Task(task_data)
    example_bot.add_task(task)
    example_bot.start_all_tasks()
