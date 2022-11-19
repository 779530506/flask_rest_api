from opensearchpy import OpenSearch
class OpenSearchClass:
    def __init__(self):
        return
     
    def createIndexTemplate(pipelinename):#pipelinename
        client = getClient()
        response = client.indices.put_template(pipelinename, {
        "template": pipelinename+"*",
        "order": 0,
        "settings": {
            "number_of_shards": 1
        },
        "mappings": {
          "properties": {
            "timestamp": {
              "type": "date",
              "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            }
          }
         }
        })
        if response.get('acknowledged'):
            return True
        else:
            return False
        
    def createIndex(pipeline_name):
        client = getClient()
        index_alias = pipeline_name
        index_name = pipeline_name+'-0001'
        index_body = {
          'settings': {
            'index': {
              'number_of_shards': 3
            },
              
          }
        }
        all_index = client.indices.get_alias().keys()
        if index_name  in all_index:
            client.indices.delete(index_name)
        response = client.indices.create(index_name, body=index_body)
        if response.get('acknowledged'):
            # on créé l'aliase
            client.indices.put_alias(index_name, index_alias)
            return True
           
        else:
            return False

def getClient():
    host = '51.77.212.74'
    port = 9200
    auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
    ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )
    return client
