from elasticsearch import Elasticsearch, RequestsHttpConnection
import curator
import os

 
# Lambda execution starts here.
def lambda_handler(event, context):

    es_host       = os.getenv('ES_HOST')
    es_password   = os.getenv('ES_PASSWORD')
    es_login      = os.getenv('ES_LOGIN')
    es_ssl        = bool(os.getenv('ES_SSL'))
    es_ssl_verify = bool(os.getenv('ES_SSL_VERIFY'))
    es_except_indices = os.getenv('ES_EXCEPT_INDICES')
    es_unit        = os.getenv('ES_UNIT')
    es_unit_count  = int(os.getenv('ES_UNIT_COUNT'))
    
    if es_login:
     es = Elasticsearch(
    hosts = [{'host': es_host , 'port': 443}],
    use_ssl = es_ssl,
    verify_certs = es_ssl_verify,
    connection_class = RequestsHttpConnection
    )
    else:
     es = Elasticsearch(
    hosts = [{'host': es_host , 'port': 443}],
    http_auth = (es_login, es_password),
    use_ssl = es_ssl,
    verify_certs = es_ssl_verify,
    connection_class = RequestsHttpConnection
    )
    

    index_list = curator.IndexList(es)
    # Delete the indices for the pattern yyyy-mm-dd* with creation_date greater than x days.
    # Source https://curator.readthedocs.io/en/latest/examples.html
    index_list.filter_by_age(source='creation_date', direction='older', timestring='%Y-%m-%d', unit=es_unit, unit_count=es_unit_count)


    def pop_used(indices,word):
        for i in index_list.indices:
            if i.find(word) == 1:
                print("Deleted itens from list:", i)
                index_list.indices.remove(i)

    for ind in es_except_indices.split(','):
        pop_used(index_list.indices, ind)
     
    print("Found %s indices to delete" % len(index_list.indices))
     
    if index_list.indices:
        curator.DeleteIndices(index_list).do_action()
     
    print('Indices deleted successfully')
