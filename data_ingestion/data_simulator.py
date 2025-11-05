import json, time, random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_patient_data(pid):
    return {
        "patient_id": pid,
        "timestamp": datetime.utcnow().isoformat(),
        "heart_rate": random.randint(60, 120),
        "systolic_bp": random.randint(100, 160),
        "diastolic_bp": random.randint(60, 100),
        "oxygen_saturation": round(random.uniform(92, 100), 1),
        "body_temp": round(random.uniform(36.0, 39.0), 1),
        "glucose_level": random.randint(70, 160)
    }

if __name__ == "__main__":
    print(" Streaming live patient vitals → Kafka topic 'raw-patient'")
    while True:
        for i in range(1, 6):
            msg = generate_patient_data(f"P{i:03}")
            producer.send('raw-patient', msg)
            print("Sent:", msg)
            time.sleep(1)
