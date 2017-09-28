#!/usr/local/bin/python3
from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time
import re

class Collector(object):

  def __init__(self, endpoint):
    self._endpoint = endpoint

  def get_broker_status(self):

    return json.loads(requests.get("http://{}/api/broker/list".format(self._endpoint)).content.decode('UTF-8'))

  def collect(self):
    # Fetch the JSON
    response = self.get_broker_status()
    metric = {}

    for broker in response['brokers']:

      task = broker['task']
      metrics = broker['metrics']
      task_id = task['id']
      endpoint = task['endpoint']
      needs_restart = broker["needsRestart"]
      
      def clean_data(data):
        return re.sub('(\.|\-)', "_", data)

      # process metrics
      for k, v in metrics.items():

        keysplit = k.split(',')
        domain = clean_data(keysplit[0])
        item = clean_data(keysplit[1]) if len(keysplit) > 1 else ""
        unit = clean_data(keysplit[2]) if len(keysplit) > 2 else ""
        if len(keysplit) > 3:
          tags = keysplit[3]
          tags = tags.split('.')
          tags = dict(zip(*([iter(tags)]*2)))
        else:
          tags = {}

        tags['broker'] = task_id
        tags['endpoint'] = endpoint

        metric_name = "_".join([domain, item, unit]).lower()
        metric_title = " ".join([domain, item, unit])

        if metric_name not in metric:
          metric[metric_name] = Metric(
            metric_name,
            metric_title,
            'gauge'
          )

        metric[metric_name].add_sample(
          metric_name,
          value=v,
          labels=tags
        )

    for x in metric.values():
       yield x    


if __name__ == '__main__':
  # Usage: kafka-mesos-exporter.py port scheduler_endpoint
  # Example: ./kafka-mesos-exporter.py 9500 kafka-scheduler-perf-3-dev-services.service.consul:31000
  start_http_server(int(sys.argv[1]))
  REGISTRY.register(Collector(sys.argv[2]))

  while True: time.sleep(1)