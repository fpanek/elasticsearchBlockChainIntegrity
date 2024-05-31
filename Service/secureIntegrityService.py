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
    secure_integrity.create_and_store_hash()
    #while True:
    #    secure_integrity.create_and_store_hash()
    #    time.sleep(1)

    #verifyIntegrity.verify_integrity("example")