import accessElastic
import accessEtherum
import verifyIntegrity
import logging
import config.config as config
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    for index in config.monitored_indices:
        verifyIntegrity.verify_integrity(index)

