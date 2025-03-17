import asyncio

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from bot import TGBot, send_message

app = FastAPI()
bot = TGBot()


# Описание ожидаемых данных
class MessageRequest(BaseModel):
    data: dict
    user_id: int


@app.post('/calculate')
def calculate(request: MessageRequest):
    params = [f'{k}={v}' for k, v in request.data.items() if v]
    requirements = ' '.join(params)
    user = request.user_id
    text = 'Copy command bellow and send to me\n'
    command_calc = f'/calculate {requirements}'
    send_message(user, text)
    send_message(user, command_calc)


async def run_fastapi():
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=80,
        log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
# WARNING:  Invalid HTTP request received.

async def main():
    loop = asyncio.get_event_loop()

    # Создаем задачи и сохраняем ссылки
    tasks = [asyncio.create_task(run_fastapi()),
             asyncio.create_task(bot.start())]

    # Обработчик для graceful shutdown
    def shutdown_handler(sig=None):
        for task in tasks:
            task.cancel()
        print("\nApplication shutdown")

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())


