import logging
from datetime import datetime
from fastapi import FastAPI
from lifen_app.views import ping, router_v0


__all__ = ["get_app"]

logger = logging.getLogger(__name__)


def get_app(startup_time: datetime) -> FastAPI:
    app = FastAPI()

    app.include_router(ping.router, prefix="", tags=["ping"])
    app.include_router(router_v0.router, prefix="", tags=["Lifen App V0"])

    @app.on_event("startup")
    async def startup():
        startup_duration_seconds = (datetime.now() - startup_time).total_seconds()
        logger.info(
            "Starting up lifen ASGI app.",
            extra={
                "startup_time": str(startup_time),
                "startup_duration_seconds": startup_duration_seconds,
            },
        )

    return app
