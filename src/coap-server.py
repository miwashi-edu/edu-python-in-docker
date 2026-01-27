#!/usr/bin/env python3
import asyncio
import aiocoap.resource as resource
import aiocoap

class Echo(resource.Resource):
    async def render_post(self, request):
        payload = request.payload or b""
        print(f"[coap-server] POST /echo: {payload.decode('utf-8', errors='replace')}")
        return aiocoap.Message(code=aiocoap.CONTENT, payload=payload)

    async def render_put(self, request):
        payload = request.payload or b""
        print(f"[coap-server] PUT /echo: {payload.decode('utf-8', errors='replace')}")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)

async def main():
    root = resource.Site()
    root.add_resource(["echo"], Echo())

    # binds UDP/5683 on all interfaces
    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0", 5683))
    print("[coap-server] listening on coap://0.0.0.0:5683/echo")

    # run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[coap-server] bye")

