import logging
from web3 import Web3
import deploy_and_verify_smart_contract
import accessElastic
import config.config as config

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.DEBUG,
  datefmt='%Y-%m-%d %H:%M:%S'
)


def verify_etherum_connectivity():
  ganache_path = f"http://{config.etherum_node_ip}:{config.etherum_node_port}"
  etherum_client = Web3(Web3.HTTPProvider(ganache_path))

  if etherum_client.is_connected():
    logging.info("Etherum connection OK")
    return True
  else:
    logging.error("Etherum connection failed!")
    return False


def verity_elastic_availability():
  single_document_query = {
    "size": 1,
    "query": {
      "match_all": {}
    }
  }
  response = accessElastic.return_result_from_database_using_body(config.database_ip, single_document_query, "example")
  if response:
    logging.info("Elastic connection OK")
    return True
  else:
    logging.error("Elastic connection failed!")
    return False




def setup():
  verify_etherum_connectivity()
  verity_elastic_availability()
  deploy_and_verify_smart_contract.verify_and_deploy_smart_contract()

