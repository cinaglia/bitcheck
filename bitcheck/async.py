from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

import requests

MAX_PARALLEL_JOBS = 3


def get(jobs):
    pool = Pool(len(jobs))
    response = pool.map(_request, jobs)
    return dict(response)


def _request(job):
    arg, service = job
    r = requests.get(service['url'])
    return (arg, service['parser'].parse(r.text))
