from uuid import uuid4
from django.conf import settings
from .tasks import boot_up
import kombu

BROKER_URL = "sqs://AKIAISFVCFWXMMT2SLDA:FzG9v5C+dGlFlJOECuqmTLFpkp3vQUv60nuk7938@"
ENVIRONMENT_NAME = settings.ENVIRONMENT_NAME
SERVER_NAME = settings.SERVER_NAME


# This stub is missing the task, the id, the kwargs, and args
STUB = {'chord': None, 'retries': 0, 'callbacks': None, 'errbacks': None, 'taskset': None, 'utc': True,
        'expires': None, 'timelimit': [None, None], 'eta': None}

"""
This is a function to send tasks between different servers.
"""


def send_task(destination, task_name, *args, **kwargs):
    conn = kombu.Connection(BROKER_URL, transport_options=dict(region='us-west-2',
                                                               queue_name_prefix=destination + '-' + str(
                                                                   ENVIRONMENT_NAME) + '-'))
    producer = kombu.Producer(conn, exchange=kombu.Exchange('celery', 'direct'), routing_key='celery')
    kwargs['source'] = SERVER_NAME
    send_dict = {'id': str(uuid4()),
                 'task': 'remote.' + task_name,
                 'args': args,
                 'kwargs': kwargs}

    # Add STUB dict to the send dict to make the full dict.
    send_dict.update(STUB)

    producer.publish(send_dict)

    conn.release()


"""
Convenience function for sending pulses.

TBH I didn't realize it would be this easy lol.
"""


def send_pulse(target):
    send_task(target, 'recieve_pulse')


"""
Convenience function for sending notifications.

TBH I didn't realize it would be this easy lol.
"""


def send_notification(title, message):
    send_task('ies-monitor', 'recieve_notification', title, message)


"""
Timeout should be in minutes.
"""


def send_ping(code, timeout):
    send_task('ies-monitor', 'recieve_ping', code, timeout)


# Code below this line should be considered defunct

boot_up.delay()
