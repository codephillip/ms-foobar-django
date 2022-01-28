import traceback

from asgiref.sync import sync_to_async
from ms_foobar_app.constants import EventSubjects, QueueGroupName

from ms_foobar_app.events.event_bus_root import EventBus
from ms_foobar_app.models import User
from ms_foobar_app.serializers import UserSerializer
from ms_foobar_app.utils.utilities import snake_case_dict_to_camel

import logging

logger = logging.getLogger(__name__)


class EventListener(EventBus):
    def __init__(self):
        super(EventListener, self).__init__()

    @sync_to_async
    def __get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    async def __user_schedule_message_handler(self, msg):
        try:
            data = self.byte_decode_data(msg.data)
            logger.debug(data)
            user = await self.__get_user_by_id(data['userId'])
            logger.debug(snake_case_dict_to_camel(UserSerializer(user).data))
            await self.sc.publish(EventSubjects.UserInfoAvailed,
                                  self.byte_encode_data(snake_case_dict_to_camel(UserSerializer(user).data)))
        except Exception:
            logger.debug(traceback.print_exc())
        finally:
            # make sure to acknowledge message receipt
            await self.sc.ack(msg)

    def subscribe(self):
        self.loop.run_until_complete(self.__subscribe())
        # never run run_forever on main thread, only run it once
        self.loop.run_forever()

    async def __subscribe(self):
        await self.sc.subscribe(EventSubjects.UserScheduleCreated, queue=QueueGroupName,
                                cb=self.__user_schedule_message_handler)
        await self.sc.subscribe(EventSubjects.PaymentCreated, queue=QueueGroupName,
                                cb=self.__user_schedule_message_handler)
