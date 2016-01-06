from .database import manager as database_manager
from .gateway import manager as gateway_manager
from .devices import manager as devices_manager
from .user import manager as user_manager

manager = gateway_manager
manager.merge(database_manager, namespace='db')
manager.merge(devices_manager, namespace='devices')
manager.merge(user_manager, namespace='users')
