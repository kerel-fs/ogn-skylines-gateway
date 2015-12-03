import logging
from ognskylines.gateway import ognSkylinesGateway
from ognskylines.dbutils import session

from manager import Manager
gateway_manager = Manager()


@gateway_manager.command
def run(skylines_host='127.0.0.1', skylines_port=5597, logfile=''):
    """Run the ogn-->skylines gateway."""

    # Enable logging
    log_handlers = [logging.StreamHandler()]
    if logfile:
        log_handlers.append(logging.FileHandler(logfile))
    logging.basicConfig(level='INFO', handlers=log_handlers)
    logging.getLogger('ognskylines').setLevel('DEBUG')

    print('Start ogn-skylines gateway')
    skylines_gateway = ognSkylinesGateway(session=session, aprs_user='skylines', host=skylines_host, port=skylines_port)

    try:
        skylines_gateway.run()
    except KeyboardInterrupt:
        print('\nStop ogn-skylines gateway')

    skylines_gateway.disconnect()
    logging.shutdown()
