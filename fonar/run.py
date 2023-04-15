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


__all__ = ["start"]

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
    def turn_on(cls, **kwargs):
        '''Включить фонарь.'''
        print('Фонарь включен')

    @classmethod
    def turn_off(cls, **kwargs):
        '''Выключить фонарь.'''
        print('Фонарь выключен')

    @classmethod
    def switch_color(cls, metadata=0):
        '''Изменить цвет фонаря.'''
        print(f'Фонарь стал цвета {metadata}')

async def fetch(client, host, port):
    async with client.get(f'http://{host}:{port}') as resp:
        assert resp.status == 200
        return await resp.json()


async def main(host=HOST, port=PORT, timeout=TIMEOUT):
    conn = aiohttp.TCPConnector()
    timeout = aiohttp.ClientTimeout(total=timeout)
    try:
        async with aiohttp.ClientSession(
                timeout=timeout,
                connector=conn
        ) as client:
            command_json = await fetch(client, host, port)
            command = command_json['command']
            metadata = command_json['metadata']

            if command in commands:
                Lamp.dispatch(command, metadata=metadata)

    except Exception as error:
        print(error)


def start(host=HOST, port=PORT, timeout=TIMEOUT):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(host=host, port=port, timeout=timeout))
    except asyncio.TimeoutError:
        print("ERROR: TIMEOUT")
    except Exception as e:
        print(e)
