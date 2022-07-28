from .models import *
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core.exceptions import ObjectDoesNotExist


def create_notification(request, sender, receiver, message):
    print(sender)
    print(receiver)
    notification = Notification.objects.create(sender=sender, receiver=receiver.user, message=message)
    channel_layer = get_channel_layer()
    import json

    data = {
        'count': notification.id,
        'sender': sender.id,
        'receiver':receiver.user.id,
        'message':message
        }
    async_to_sync(channel_layer.group_send)(
        'notification_1', {
            'type': 'send_notification',
            'value': json.dumps(data)
        }
    )
