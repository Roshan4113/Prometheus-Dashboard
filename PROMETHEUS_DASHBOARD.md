# Prometheus Dashboard

This repository contains resources and instructions to create and import a Grafana dashboard backed by Prometheus metrics.

## Overview

This document explains how to use, import, and maintain a Grafana dashboard that visualizes metrics collected by Prometheus. It includes recommended panels, example PromQL queries, and sample alerting rules that you can add to Prometheus Alertmanager.

## Prerequisites

- Prometheus instance collecting metrics from your applications and infrastructure
- Grafana (v7+ recommended)
- A Prometheus datasource configured in Grafana (name: `Prometheus` or update queries accordingly)

## Importing the Dashboard into Grafana

1. In Grafana, go to + Create → Import.
2. Either upload the dashboard JSON file (if this repo includes a JSON in `dashboards/`) or paste the JSON contents into the text field.
3. Select the Prometheus data source configured in your Grafana instance.
4. Click Import.

If you do not yet have a JSON file, you can create a new dashboard in Grafana, add panels using the PromQL examples below, then save and export the dashboard JSON into this repo under `dashboards/`.

## Recommended Panels and Example PromQL Queries

Replace the data source or metric names to match your environment.

- CPU Usage (instance)
  - Query: `100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
  - Visualization: Time series (line)

- Memory Usage (instance)
  - Query: `100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes)))`
  - Visualization: Gauge or time series

- Disk Utilization (per mount)
  - Query: `100 - (node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} * 100 / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"})`
  - Visualization: Time series or single stat

- Network Throughput (bytes/sec)
  - Query (receive): `sum by (instance) (rate(node_network_receive_bytes_total[5m]))`
  - Query (transmit): `sum by (instance) (rate(node_network_transmit_bytes_total[5m]))`

- HTTP Request Rate (app)
  - Query: `sum by (job) (rate(http_requests_total[5m]))`

- Error Rate (app)
  - Query: `sum by (job) (rate(http_requests_total{status=~"5.."}[5m])) / sum by (job) (rate(http_requests_total[5m]))`

- Custom Application Metric (example)
  - Query: `myapp_jobs_processed_total` or rate over time: `rate(myapp_jobs_processed_total[5m])`

## Alerting Examples (Prometheus Rule YAML)

Save rules under `prometheus/rules/` and reload Prometheus or use file-based rule configs.

example-alerts.yaml

```yaml
groups:
  - name: node.rules
    rules:
      - alert: InstanceDown
        expr: up == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Instance {{ $labels.instance }} down"
          description: "Prometheus target {{ $labels.instance }} has been down for more than 5 minutes."

      - alert: HighCpuUsage
        expr: 100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100) > 90
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is >90% for more than 10 minutes."
```

Adjust `for`, thresholds, and labels to match your operational needs.

## Directory suggestions

- `dashboards/` - store exported Grafana JSON files
- `prometheus/` - Prometheus scrape configs and alerting rule files
- `docs/` - additional documentation

## Tips and Best Practices

- Use recording rules in Prometheus to precompute expensive queries used by dashboards.
- Keep dashboard JSONs small and modular; split into multiple dashboards if necessary.
- Use template variables in Grafana (e.g., `instance`, `job`) for flexible reuse across environments.
- Add dashboard versioning and change log in this repo whenever you update exported JSON.

## Contributing

If you add or update dashboards, please:

1. Export the dashboard JSON from Grafana and add it under `dashboards/` with a meaningful filename.
2. Update this markdown with any new panels or important PromQL used.
3. Open a pull request with a summary of changes.

## References

- Prometheus: https://prometheus.io/
- Grafana: https://grafana.com/
