"""
Stresstest the API
"""

import random

from locust import HttpLocust, TaskSet, between, task


class MakeCall(TaskSet):

    @task
    def request_banner(self):
        n = random.randint(1, 50)
        self.client.get(f'/campaigns/{n}')


class APIUser(HttpLocust):
    task_set = MakeCall
    wait_time = between(1, 4)
