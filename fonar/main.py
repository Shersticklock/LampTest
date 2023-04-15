import aiohttp
import asyncio
import enum

HOST = '127.0.0.1'
PORT = 9999
TIMEOUT = 5

class Commands(enum.Enum):
    ON = 'ON'
    OFF = 'OFF'
    COLOR = 'COLOR'

commands = (
    Commands.ON.value,
    Commands.OFF.value,
    Commands.COLOR.value
)


class Lamp:
    @classmethod
    def dispatch(cls, command, **kwargs):
        commands = {
            Commands.ON.value: cls.turn_on,
            Commands.OFF.value: cls.turn_off,
            Commands.COLOR.value: cls.switch_color
        }
        function = commands.get(command, None)
        if function is None:
            return
        function(**kwargs)

    @classmethod
    def turn_on(cls):
        '''Включить фонарь.'''
        print('Фонарь включен')

    @classmethod
    def turn_off(cls):
        '''Выключить фонарь.'''
        print('Фонарь выключен')

    @classmethod
    def switch_color(cls, metadata=0):
        '''Изменить цвет фонаря.'''
        print(f'Фонарь стал цвета {metadata}')

async def fetch(client):
    async with client.get(f'http://{HOST}:{PORT}') as resp:
        assert resp.status == 200
        return await resp.json()


async def main():
    conn = aiohttp.TCPConnector()
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    try:
        async with aiohttp.ClientSession(
                timeout=timeout,
                connector=conn
        ) as client:
            command_json = await fetch(client)
            command = command_json['command']
            metadata = command_json['metadata']

            if command in commands:
                Lamp.dispatch(command, metadata=metadata)

    except aiohttp.client_exceptions.ClientConnectorError as error:
        print(error)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except asyncio.TimeoutError:
        print("ERROR: TIMEOUT")
    finally:
        loop.close()
