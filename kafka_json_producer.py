import pandas as pd
from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer ,SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer


FILE_PATH = "\\Users\\sahee\\OneDrive\\Desktop\\Big Data Bootcamp\\Live Class notes\\11 - Oct 1 - Kafka Class 2\\Kafka - Assignment\\restaurant_orders.csv"
columns=['order_number', 'order_date', 'item_name', 'quantity', 'product_price', 'total_products']

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

def delivery_message(err,msg):
    if err:
        print("Record",msg.key(),"couldn't be produced because of",err)
    else:
        print('User record {} successfully produced to TOPIC {}, partition [{}] at offset {}'.format(\
            msg.key(), msg.topic(), msg.partition(), msg.offset()))
            
            
def main(topic):
    schema_conf=schema_config()
    schema_reg_client= SchemaRegistryClient(schema_conf)
    
    schemaStr= schema_reg_client.get_latest_version(topic+"-value").schema.schema_str
    
    
    stringser= StringSerializer()
    jsonser= JSONSerializer(schemaStr, schema_reg_client)
    
    producer = Producer(sasl_conf())

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    
    producer.poll(0.0)
    
    
    try:
        df=pd.read_csv(FILE_PATH)
        df=df.iloc[:,:]
        
        columns= list(df.columns)
       
        
        for data in df.values:
            
            row= dict(zip(columns,data))
            #print(row)
            producer.produce(topic=topic,
                            key=stringser(str(uuid4()), SerializationContext(topic, MessageField.KEY)),
                            value=jsonser(row, SerializationContext(topic, MessageField.VALUE)),
                            on_delivery=delivery_message)
            
    except KeyboardInterrupt:
        pass
    except ValueError:
        print("Invalid input, discarding record...")
        pass

    print("\nFlushing records...")
    producer.flush()
    
    
    
main('restaurant-take-away-data')