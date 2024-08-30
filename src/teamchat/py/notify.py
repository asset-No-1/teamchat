from kafka import KafkaProducer
import json

def producer_alarm(*args):
    producer=KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    #airflow log상에서 print 잘 되나 확인
    print(args[0])

    message = args[0]
    data={'bot': message}
    producer.send('Product', value=data)
    producer.flush()

