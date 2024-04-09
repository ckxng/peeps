#!/usr/bin/env python3

import argparse
import asyncio
import logging
from functools import partial
from typing import Optional

import websockets
from websockets.server import serve

from lib.player import Player
from lib.region import Region

logger = logging.getLogger('websockets')
logger.addHandler(logging.StreamHandler())

CONNECTIONS = set()
WATCHERS = {}


async def respond(websocket, region):
    CONNECTIONS.add(websocket)
    player: Optional[str] = None
    try:
        async for message in websocket:
            if player is None and message[:6] == 'login ':
                player = message[6:]
            elif player is not None:
                if message == 'want_sensor_data':
                    if player not in WATCHERS:
                        WATCHERS[player] = set()
                    WATCHERS[player].add(websocket)
                    await websocket.send(f"watching {player} sensors")
                elif message == 'no_want_sensor_data':
                    WATCHERS[player].remove(websocket)
                elif message == 'json':
                    await websocket.send(region.to_json())
                elif message == 'compressed_json':
                    await websocket.send("compressed_sensor_data " + region.to_compressed_json())
            else:
                await websocket.send(f"invalid")
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)
        if player is not None:
            WATCHERS[player].remove(websocket)


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
    parser.add_argument('-t', '--timer', type=int, default=1)
    return parser.parse_args()


async def simulate(region, timer):
    step = 1
    while True:
        websockets.broadcast(CONNECTIONS, f"step {step}")
        for player in WATCHERS:
            for ws in WATCHERS[player]:
                await ws.send("compressed_sensor_data " + region.to_compressed_json())
        await asyncio.sleep(timer)
        region.step()
        step += 1


async def main():
    args = await parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    p = Player()
    r = Region(seed=args.seed, controller=p)

    ws_task = asyncio.create_task(start_server(r, args.host, args.port))
    sim_task = asyncio.create_task(simulate(r, args.timer))

    await asyncio.gather(
        ws_task,
        sim_task,
    )


if __name__ == '__main__':
    asyncio.run(main())
