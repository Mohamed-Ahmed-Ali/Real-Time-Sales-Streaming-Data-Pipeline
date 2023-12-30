# plugins/operators/kafka_producer_operator.py
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from kafka import KafkaProducer
import json


class KafkaProducerOperator(BaseOperator):
    template_fields = ('message',)
    
    @apply_defaults
    def __init__(self, bootstrap_servers, topic, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.message = message

    def execute(self, context):
        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        producer.send(self.topic, value=self.message)
        producer.flush()
