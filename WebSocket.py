import asyncio
import websockets
import json
import sys
import os
import signal
from websockets import exceptions
users = {}


async def handler(websocket):
    while True:
        connections = list(users.values())
        usernames = list(users.keys())
        try:
            message = await websocket.recv()
        except exceptions.ConnectionClosedOK:
            print("Connection closed")
            # delete user from list
            for k, v in users.items():
                if v == websocket:
                    users.pop(k)
                    event = {
                        "type": "message",
                        "body": "Disconnected: " + k
                    }
                    websockets.broadcast(connections, json.dumps(event))
                    break

            # send updated list to all
            usernames = list(users.keys())
            event = {
                "type": "users",
                "body": usernames
            }
            websockets.broadcast(connections, json.dumps(event))

            break

        event = json.loads(message)
        print(event)
        if event["type"] == "changedName":
            oldname = event["oldname"]
            name = event["name"]
            event = {
                "type": "message",
                "body": f"{oldname} changed name to {name}"
            }
            websockets.broadcast(connections, json.dumps(event))
            users.update({name: websocket})
            connections = list(users.values())
            usernames = list(users.keys())
            event = {
                "type": "users",
                "body": usernames
            }
            websockets.broadcast(connections, json.dumps(event))
            continue

        if event["type"] == "message":
            name = event["name"]
            mess = f"{name}: {event['body']}"
            # переотправляем остальным участникам
            event = {
                "type": "message",
                "body": mess
            }
            websockets.broadcast(connections, json.dumps(event))
            continue

        if event["type"] == "joining":
            name = event["name"]
            event = {
                "type": "message",
                "body": f"Поприветсвуем {name}!"
            }
            websockets.broadcast(connections, json.dumps(event))
            users.update({name: websocket})
            connections = list(users.values())
            usernames = list(users.keys())
            event = {
                "type": "users",
                "body": usernames
            }
            websockets.broadcast(connections, json.dumps(event))
            continue


async def main(host):
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    port = int(os.environ.get("PORT", "8081"))
    async with websockets.serve(handler, host, port):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Ctrl + C to end.\n\tStarted at " + str(sys.argv[1]) + ":8081")
        try:
            asyncio.run(main(str(sys.argv[1])))
        except KeyboardInterrupt:
            print("KeyboardInterrupt now you can exit")
            input("press enter")
            exit(0)
    else:
        print("Ctrl + C to end.\n\tStarted at localhost:8081")
        try:
            asyncio.run(main("localhost"))
        except KeyboardInterrupt:
            print("KeyboardInterrupt now you can exit")
            input("press enter")
            exit(0)