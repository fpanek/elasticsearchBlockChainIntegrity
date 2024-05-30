import setup

import config
import accessElastic
import createChecksum
import accessEtherum
import setup

def insert_test_document():
    document_body = {
        "@timestamp": "2024-05-30T12:34:56Z",
        "title": "Testing insert functionality",
        "content": "Test insert 0001"
    }
    response = accessElastic.insert_document("10.0.13.3", "example", "M8mmu48BV3C7FM5ly935", document_body)
    print(response)


def updating_test_document():
    document_body = {
        "integrity_checksum_created": True
    }
    response = accessElastic.update_document("10.0.13.3", "example", "M8mmu48BV3C7FM5ly935", document_body)
    print(response)

def get_test_result_from_database():
    query = {"bool": {"must_not": [{"exists": {"field": "integrity_checksum_created"}}]}}
    response = accessElastic.return_result_from_database("10.0.13.3", query, "example")
    for hit in response['hits']['hits']:
       print(hit)


def test_deploy_smart_contract():
    contract = accessEtherum.compile_and_deploy("SimpleKeyValueStorage.sol")
    print("Contract deployed at:", contract.address)

def test_contract_exist(contract_address):
    accessEtherum.verify_contract(contract_address)

def test_store_and_retrieve_value_from_contract(contract):
    accessEtherum.set_key_value(contract, 'hello', 'world')
    value = get_value(contract, 'hello')
    print('Stored value retrieved from Blockchain:', value)


if __name__ == '__main__':
    #insert_test_document()
    #updating_test_document()
    #get_test_result_from_database()
    #accessEtherum.iterate_through_all_blocks()
    #test_deploy_smart_contract();
    #contract_address = "0xBF5B6ED6c1D001b9E151053872B89c6ba36A09eA"
    #contract_result = test_contract_exist(contract_address)
    #test_store_and_retrieve_value_from_contract()
    setup.setup()

