#configuration file

database_ip="10.0.13.3"
database_port=9200
database_username="elastic"
database_password="waV*9dIjpiXnz*6tgTT1"
monitored_indices=["test-*"]
polling_interval=10 #polling interval for  elastic database changes in seconds
verify_certs=False

etherum_node_ip="127.0.0.1"
etherum_node_port="7545"

##test parameters
test_index = "test-2024-05"
#existing_contract_address = "0x1234567890abcdef1234567890abcdef12345678"
existing_contract_address = "0x1Fd96C0e680bc2904dFf96957EF3f421dF244C8E" #from ganache
