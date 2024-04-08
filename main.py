#!/usr/bin/env python3

import argparse
import asyncio
import logging
from functools import partial

from websockets.server import serve

from lib.player import Player
from lib.region import Region

logger = logging.getLogger('websockets')
logger.addHandler(logging.StreamHandler())


async def respond(websocket, region):
    async for message in websocket:
        if message == 'json':
            await websocket.send(region.to_json())
        elif message == 'compressed_json':
            await websocket.send(region.to_compressed_json())
        else:
            await websocket.send(f"echo: {message}")


async def start_server(region: Region, host: str, port: int):
    async with serve(partial(respond, region=region), host=host, port=port):
        await asyncio.Future()


async def parse_args():
    parser = argparse.ArgumentParser(
        prog='peeps',
        description='Simulate a world of little peeps',
        epilog='All your base are belong to us.',
    )
    parser.add_argument('-s', '--seed', type=int, default=None)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-H', '--host', type=str, default='0.0.0.0')
    parser.add_argument('-P', '--port', type=int, default='8080')
    return parser.parse_args()


async def simulate(region):
    while True:
        region.step()
        await asyncio.sleep(1)


async def main():
    args = await parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    p = Player()
    r = Region(seed=args.seed, controller=p)

    ws_task = asyncio.create_task(start_server(r, args.host, args.port))
    sim_task = asyncio.create_task(simulate(r))

    await asyncio.gather(
        ws_task,
        sim_task,
    )


if __name__ == '__main__':
    asyncio.run(main())
