from .insert import manager as insert_manager
from .show import manager as show_manager

manager = insert_manager
manager.merge(show_manager, namespace='')
