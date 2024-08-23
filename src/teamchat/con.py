from kafka import KafkaConsumer, TopicPartition
import pyarrow.parquet as pq
import os

def read_parquet_records(parquet_file):
        table = pq.read_table(parquet_file)
        schema = table.schema
        records = table.to_pandas()
    
        
        
        #for _, record in records.iterrows():
        #    message = record.to_json()
        #   producer.send('your_topic_name', value=message.encode(), key=None)


consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        consumer_timeout_ms=5000,
        group_id="movie",
        enable_auto_commit=False,
)


p = TopicPartition('movie', 0)
consumer.assign([p])

if saved_offset is not None:
    consumer.seek(p, saved_offset)
else:
    consumer.seek_to_beginning(p) #저장된 오프셋이 없으면 처음부터 읽기

for m in consumer:
    print(f"offset={m.offset}, value={m.value}")
    save_offset(m.offset + 1)
