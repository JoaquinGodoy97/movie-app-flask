# logger.py
import logging

# Configure logging
logger = logging.getLogger("./my_app")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)