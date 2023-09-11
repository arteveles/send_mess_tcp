import asyncio
from typing import Optional
from threading import Thread


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost, request_count=1):
        self.message = message
        self.on_con_lost = on_con_lost
        self._transport: Optional[asyncio.Transport] = None
        self.count = 0
        self.request_count = request_count


    def connection_made(self, transport: asyncio.Transport):
        self._transport = transport
        self._transport.write(self.message)
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        if self.count >= self.request_count:
            self._transport.close()
        self.count += 1
        self._transport.write(self.message)
        print('Data received: {!r}'.format(data))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main(count_message):
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    for i in range(count_message):
        with open(f'dev/adviser_tcp_protocol_{i}.bin', 'rb') as file:
            data = file.read()
        transport, protocol = await loop.create_connection(lambda: EchoClientProtocol(data, on_con_lost, request_count=2),'0.0.0.0', 5002)
        transport.close()


if __name__ == "__main__":
    asyncio.run(main(3))
