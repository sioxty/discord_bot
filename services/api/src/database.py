import asyncio
from dataclasses import dataclass
import logging
import os
import motor.motor_asyncio
from .Types import UserModel
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv('DATABASE')
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE)
db = client["discord"]
collection = db["users"]
log = logging.getLogger(__name__)


