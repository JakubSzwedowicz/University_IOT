from Utils.common import Connection, TOPIC


class Subscriber(Connection):
    def __init__(self):
        super().__init__()

    def connect(self):
        super().connect()
        self.client.on_message = self.process_message
        self.client.loop_start()

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    @staticmethod
    def process_message(client, userdata, message):
        card_uid, log_time = str(message.payload.decode('utf-8')).split(';')
        print(f'Received: "{card_uid}" registered at: "{log_time}"')


if __name__ == '__main__':
    sub = Subscriber()
    sub.connect()
    sub.subscribe(TOPIC)

    while True:
        pass
