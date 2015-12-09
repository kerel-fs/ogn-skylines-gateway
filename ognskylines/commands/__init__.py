from .database import manager as database_manager
from .gateway import manager as gateway_manager

manager = gateway_manager
manager.merge(database_manager, namespace='db')
