import config
import motor.motor_asyncio

conn = motor.motor_asyncio.AsyncIOMotorClient(config.mongoConnectUrl)
db = conn[config.mongoDataBase]