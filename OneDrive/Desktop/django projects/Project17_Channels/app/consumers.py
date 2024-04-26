import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('WebSocket Connected')
        self.send({
            'type': 'websocket.accept',
        })

    def websocket_receive(self, event):
        print('Data received :', event['text'])
        print("Channel Layer ", self.channel_layer)
        print("Channel Name ", self.channel_name)
        self.channel_layer.group_add('programmers', self.channel_name)
        msg = json.loads(event['text'])
        self.channel_layer.group_send('programmers', {
            'type': 'chat.message',
            'message': msg
        })

    async def chat_message(self, event):
        print('Event:', event['message'])
        msg = json.dumps(event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': msg
        })

    async def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)('programmers', self.channel_name)
        print('WebSocket Disconnected')
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('WebSocket Connected')

        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        username = self.scope['user'].username
        if username == "":
            username = "Anonymous User"
        print(username)
        if self.scope['user'].is_authenticated:
            group_name = self.scope['url_route']['kwargs']['group']
            await self.channel_layer.group_add(group_name, self.channel_name)
            # event['username'] = username
            msg = json.loads(event['text'])
            msg['username'] = username
            await self.channel_layer.group_send(group_name, {
                'type': 'chat.message',
                'message': msg,
                'group': group_name,
            })
        else:
            msg = {"msg": "Login required", "username": username}  # Construct message object
            print(username)
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(msg),

            })

    async def chat_message(self, event):
        print('Event:', event['message'], type(event['message']))
        msg = json.dumps(event['message'])
        print("Group Name:", event['group'])

        # try:
        #     group = Group.objects.get(name=event['group'])
        #     chat = Chat.objects.create(message=msg, group=group)
        #
        # except Group.DoesNotExist:
        #     print("Group does not exist:", event['group'])
        # except Exception as e:
        #     print("Error:", e)
        # #
        await self.send({
            'type': 'websocket.send',
            'text': msg
        })

    async def websocket_disconnect(self, event):
        group_name = self.scope['url_route']['kwargs']['group']
        await self.channel_layer.group_discard(group_name, self.channel_name)
        print('WebSocket Disconnected')
        raise StopConsumer()
