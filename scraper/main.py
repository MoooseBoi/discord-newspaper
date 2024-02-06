import os
from kafka import KafkaConsumer


def main():
    consumer = KafkaConsumer(os.getenv("REQUEST_TOPIC"))

    for request in consumer:
        print(request)

        # add handler logic here


if __name__ == "__main__":
    main()
