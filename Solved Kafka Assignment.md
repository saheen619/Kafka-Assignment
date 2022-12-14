1. Setup Confluent Kafka Account:

![Setup_Account/Login](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/Setup-Login%20Kafka%20Account.JPG?raw=true)




2. Create one kafka topic named as "restaurant-take-away-data" with 3 partitions

![Setup_Account/Login](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/Topic%20creation%20with%203%20partitions.JPG?raw=true)




3. Setup key (string) & value (json) schema in the confluent schema registr

![Setup_Key(string) & Value(Json) Schema](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/Setup%20Key(string)%20&%20Value(JSON)%20Schema.JPG?raw=true)


4. Write a kafka producer program (python or any other language) to read data records from restaurent data csv file, 
   make sure schema is not hardcoded in the producer code, read the latest version of schema and schema_str from schema registry and use it for
   data serialization.
   
   https://github.com/saheen619/Kafka-Assignment/blob/main/kafka_json_producer.py

5. From producer code, publish data in Kafka Topic one by one and use dynamic key while publishing the records into the Kafka Topic.

![Publish Data in Kafka Topic](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/Publish%20Data%20in%20Kafka%20Topic.JPG?raw=true)

6. Write kafka consumer code and create two copies of same consumer code and save it with different names (kafka_consumer_1.py & kafka_consumer_2.py), 
   again make sure latest schema version and schema_str is not hardcoded in the consumer code, read it automatically from the schema registry to desrialize the data. 
   Now test two scenarios with your consumer code:
   
    a.) Use "group.id" property in consumer config for both consumers and mention different group_ids in kafka_consumer_1.py & kafka_consumer_2.py,
        apply "earliest" offset property in both consumers and run these two consumers from two different terminals. Calculate how many records each consumer
        consumed and printed on the terminal
        
      The consumer codes with DIFFERENT group id's are below: 
      
      https://github.com/saheen619/Kafka-Assignment/tree/main/Consumer%20Files%20-%20Different%20Group_id
        
      The consumer lag dashboard in Kafka for group 1 while consumption in progress is as below:
        ![consumer_lag_g1](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/group1_consumer_lag.JPG?raw=true)
        
      The consumer lag dashboard in Kafka for group 2 while consumption in progress is as below:
        ![consumer_lag_g2](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/group2_consumer_lag.JPG?raw=true)
        
      After execution of both consumer codes with DIFFERENT Group ID's:
        ![consumer_diff_groupid](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/Consumer_with_diff_group_id.JPG?raw=true)
        
    b.) Use "group.id" property in consumer config for both consumers and mention same group_ids in kafka_consumer_1.py & kafka_consumer_2.py,
        apply "earliest" offset property in both consumers and run these two consumers from two different terminals. Calculate how many records each consumer
        consumed and printed on the terminal
        
      The consumer codes with SAME group id's are below:
      
      https://github.com/saheen619/Kafka-Assignment/tree/main/Consumer%20Files%20-%20Same%20Group_id
        
      After execution of both consumer codes with SAME Group ID's:
        ![consumer_same_groupid](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/Consumer_with_same_group_id.JPG?raw=true)

        
7. Once above questions are done, write another kafka consumer to read data from kafka topic and from the consumer code create one csv file "output.csv"
   and append consumed records output.csv file

![consumed and created output.csv](https://github.com/saheen619/Kafka-Assignment/blob/main/Screenshots/Append%20Records%20in%20Output%20File.JPG?raw=true)

The created output.csv file is as below:

https://github.com/saheen619/Kafka-Assignment/blob/main/output.csv
