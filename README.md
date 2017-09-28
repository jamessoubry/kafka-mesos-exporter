
# Kafka Mesos Exporter for Prometheus

This is a *prometheus* (http://www.prometheus.io) *exporter* (https://prometheus.io/docs/instrumenting/exporters/) for *kafka-mesos* (http://kafka.mesosframeworks.com/)

Based on Brian Brazil's:

    https://www.robustperception.io/writing-json-exporters-in-python/

It scrapes the kafka-mesos scheduler's api for broker metrics:

```
curl http://kafka-scheduler/api/broker/list
```

You can run directly:
```
./kafka-mesos-exporter.py 8080 kafka-sheduler:8081 &
curl localhost:8080
```


Or through docker https://hub.docker.com/r/jamessoubry/kafka-mesos-exporter/:
```
docker run -p 8080:8080 jamessoubry/kafka-mesos-exporter 8080 kafka-sheduler:8081
curl localhost:8080
```