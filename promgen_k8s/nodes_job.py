
from prom_dsl import *

class NodesJob:
  def __init__(self, additional_relabel_configs=[], additional_metric_relabel_configs=[]):
    self.type = 'nodes'
    self.additional_relabel_configs = additional_relabel_configs
    self.additional_metric_relabel_configs = additional_metric_relabel_configs

  # Scrape config for nodes (kubelet).
  #
  # Rather than connecting directly to the node, the scrape is proxied though the
  # Kubernetes apiserver.  This means it will work if Prometheus is running out of
  # cluster, or can't connect to nodes for some other reason (e.g. because of
  # firewalling).
  def generate(self, prom_conf, c):
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-nodes'.format(c.name),
      'scheme': 'https',
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('node') ],

      # This TLS & bearer token file config is used to connect to the actual scrape
      # endpoints for cluster components. This is separate to discovery auth
      # configuration because discovery & scraping are two separate concerns in
      # Prometheus. The discovery auth config is automatic if Prometheus runs inside
      # the cluster. Otherwise, more config options have to be provided within the
      # <kubernetes_sd_config>.
      'tls_config': { 'ca_file': c.ca_file },
      'bearer_token_file': c.bearer_token_file,

      # Keep all node labels without their prefix, proxy against apiserver with
      # HTTPS by default
      'relabel_configs': [
        labelmap(regex='__meta_kubernetes_node_label_(.+)'),
        set_value('__address__', '{0}:443'.format(c.api_server)),
        replace(source_labels=['__meta_kubernetes_node_name'],
          regex='(.+)', replacement='/api/v1/nodes/${1}/proxy/metrics',
          target_label='__metrics_path__')
      ],

      'metric_relabel_configs': [
        drop(source_labels=['__name__'], regex='go_.*')
      ]
    })

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'].extend(self.additional_metric_relabel_configs)
