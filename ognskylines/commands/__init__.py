from .database import database_manager
from .gateway import gateway_manager

manager = gateway_manager
manager.merge(database_manager, namespace='db')
