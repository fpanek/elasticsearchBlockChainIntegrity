import accessElastic
import accessEtherum
import verifyIntegrity
import logging
import config.config as config
import time
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    start_time = time.time()
    for index in config.monitored_indices:
        logging.info(f"Start verification of Index {index}")
        verifyIntegrity.verify_integrity(index)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Verifying integrity took {elapsed_time} seconds")
