from ms_foobar_app.events.event_bus_root import EventBus


class EventPublisher(EventBus):
    def __init__(self):
        super(EventPublisher, self).__init__()

    def publish(self, subject, data):
        self.loop.run_until_complete(self.__publish(subject, data))

    async def __publish(self, subject, data):
        await self.sc.publish(subject, self.byte_encode_data(data))
