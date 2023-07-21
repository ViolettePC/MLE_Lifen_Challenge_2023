from datetime import datetime
from .app import get_app

STARTUP_TIME = datetime.now()


app = get_app(startup_time=STARTUP_TIME)
