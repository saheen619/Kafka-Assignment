import pandas as pd
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer

import json



FILE_PATH = "\\Users\\sahee\\OneDrive\\Desktop\\Big Data Bootcamp\\Live Class notes\\11 - Oct 1 - Kafka Class 2\\Kafka - Assignment\\restaurant_orders.csv"


API_KEY = 'FBB3BBFVI5WNJCIV'
ENDPOINT_SCHEMA_URL  = 'https://psrc-6zww3.us-east-2.aws.confluent.cloud'
API_SECRET_KEY = 'JZSCc9nq292/9jICada9INoJSzpaxTSAQ4z3hx6EIe25hYdYl6Hswlmjv2S72fq1'
BOOTSTRAP_SERVER = 'pkc-ymrq7.us-east-2.aws.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = 'TQFPEIBCZLCJVGUK'
SCHEMA_REGISTRY_API_SECRET = 'iyP0ADULQgoGnPiDKVs5xgUuxSvDcRod1oztDn6Gm2CA6eFY/or4KW0MRKd98z+v'


def sasl_conf():

    sasl_conf = {'sasl.mechanism': SSL_MACHENISM,
                'bootstrap.servers':BOOTSTRAP_SERVER,
                'security.protocol': SECURITY_PROTOCOL,
                'sasl.username': API_KEY,
                'sasl.password': API_SECRET_KEY
                }
    return sasl_conf

def schema_config():
    return {'url':ENDPOINT_SCHEMA_URL,
    
    'basic.auth.user.info': f'{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}'

    }


def main(topic):
    schema_registry_conf= schema_config()
    schema_registry_client= SchemaRegistryClient(schema_registry_conf)
    
    schemaStr= schema_registry_client.get_latest_version(topic+"-value").schema.schema_str
    
    cols= list(json.loads(schemaStr)['properties'].keys())
    
    
    json_deserializer= JSONDeserializer(schemaStr)
    
    consumer_conf = sasl_conf()
    consumer_conf.update({
                     'group.id': 'group2',
                     'auto.offset.reset': "earliest"})

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    
    totalrecords= 0
    
    output= pd.DataFrame(columns=cols)
    
    
    while True:
        try:
            
            msg = consumer.poll(0.1)
            if msg is None:
                continue

            row = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            
          
            dff=pd.DataFrame([row])
            output=pd.concat([output,dff])
            
            

            if row is not None:
                print("User record {}: car: {}, partition: {}, offset: {} \n"
                      .format(msg.key(), row, msg.partition(), msg.offset() ))
                totalrecords+=1
        except KeyboardInterrupt:
            print("---------------------\n Total records read= ",totalrecords,'\n-----------------------')
            
            break

    consumer.close()
    

    
main('restaurant-take-away-data')