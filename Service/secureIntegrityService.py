import logging
import time
import secure_integrity

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S'
)


if __name__ == '__main__':
    start_time = time.time()
    secure_integrity.create_and_store_hash()
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Securing integrity took {elapsed_time} seconds")
    #while True:
    #    secure_integrity.create_and_store_hash()
    #    time.sleep(1)

    #verifyIntegrity.verify_integrity("example")