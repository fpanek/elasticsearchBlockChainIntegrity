import logging
import hashlib
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.DEBUG,
  datefmt='%Y-%m-%d %H:%M:%S'
)

def create_checksum(*args):
    text = "".join(str(arg) for arg in args if arg is not None)
    logging.debug(f"Creating Checksum for  {text}")
    hash_object = hashlib.sha256()
    hash_object.update(text.encode('utf-8'))
    checksum = hash_object.hexdigest()
    logging.debug(f"Resulted in Checksum {checksum}")
    return checksum