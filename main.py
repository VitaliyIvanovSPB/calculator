import asyncio
from fastapi import FastAPI
import uvicorn
from bot import run_bot
import signal

app = FastAPI()


@app.get("/")
async def health_check():
    return {"status": "ok"}


async def run_fastapi():
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    loop = asyncio.get_event_loop()

    # Создаем задачи и сохраняем ссылки
    tasks = [
        asyncio.create_task(run_fastapi()),
        asyncio.create_task(run_bot())
    ]

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