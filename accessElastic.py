import config.config as config
from elasticsearch import Elasticsearch


import logging
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.DEBUG,
  datefmt='%Y-%m-%d %H:%M:%S'
)

def return_result_from_database(ip, query, index_name):
    logging.debug(f"Connecting to elastic database: {ip}, {query},  {index_name}")
    host_url = f"https://{ip}:{config.database_port}"
    client = Elasticsearch (
        [host_url],
        verify_certs=config.verify_certs,
        basic_auth=(config.database_username, config.database_password)
    )
    logging.debug(f"Executing get query: {query} onto index: {index_name}")
    try:
        response = client.search(index=index_name, size=config.documents_to_query_at_once, query=query)
    except Exception as e:
        response = e
    return response

def return_result_from_database_using_body(ip, body, index_name):
    logging.debug(f"Connecting to elastic database: {ip}, {body},  {index_name}")
    host_url = f"https://{ip}:{config.database_port}"
    client = Elasticsearch (
        [host_url],
        verify_certs=config.verify_certs,
        basic_auth=(config.database_username, config.database_password)
    )
    logging.debug(f"Executing get query: {body} onto index: {index_name}")
    response = client.search(index=index_name, body=body)
    return response


def return_limited_result_from_database(ip, query, index_name, size):
    logging.debug(f"Connecting to elastic database: {ip}, {query}, {index_name}")
    host_url = f"https://{ip}:{config.database_port}"
    client = Elasticsearch(
        [host_url],
        verify_certs=config.verify_certs,
        basic_auth=(config.database_username, config.database_password)
    )
    logging.debug(f"Executing get query: {query} onto index: {index_name}")
    try:
        response = client.search(index=index_name, size=size, body=query)
    except Exception as e:
        logging.error(f"Search query failed: {str(e)}")
        response = e
    return response

def insert_document(ip, index_name, document_id, document_body): #if document_id is empty a new documment id is automatically created if a new document is inserted
    logging.debug(f"Inserting into index: {index_name}, document: {document_body}")
    host_url = f"https://{ip}:{config.database_port}"
    client = Elasticsearch(
        [host_url],
        verify_certs=config.verify_certs,
        basic_auth=(config.database_username, config.database_password)
    )
    logging.debug(f"Inserting document {document_body} into index {index_name}")
    response = client.index(index=index_name, id=document_id, document=document_body)
    return response

def update_document(ip, index_name, document_id, new_field_data): #if document_id is empty a new documment id is automatically created if a new document is inserted
    logging.debug(f"Updating document id: {document_id}, content: {new_field_data}")
    host_url = f"https://{ip}:{config.database_port}"
    update_body = {
        "doc": new_field_data
    }
    client = Elasticsearch(
        [host_url],
        verify_certs=config.verify_certs,
        basic_auth=(config.database_username, config.database_password)
    )
    logging.debug(f"Updating document: {document_id}, new data: {new_field_data} from index {index_name}")
    response = client.update(index=index_name, id=document_id, body=update_body)
    return response




