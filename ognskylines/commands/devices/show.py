from ognskylines.model.functions import show_seen_devices, show_nearby_devices, NoResultFound

from formatter import format_fuzzy_direction, format_distance

from manager import Manager
manager = Manager()


@manager.command
def show_all():
    """Show all devices with known location."""
    try:
        devices = show_seen_devices()
    except NoResultFound:
        print('No devices with location in the databse.')
    else:
        print('{:^11} | {:^23}'.format('ogn address', 'Location'))
        print('{:-<11} | {:-<23}'.format('', ''))
        for device in devices:
            print("{:>11} | {: 7.4f}, {:8.4f}".format(
                device['ogn_address'],
                device['location']['lat'],
                device['location']['lon']))


@manager.arg('lat', help='Latitude of your location')
@manager.arg('lon', help='Longitude of your location')
@manager.arg('r', help='Search radius in km')
@manager.arg('n', help='Limit output to N entries')
@manager.command
def show_nearby(lat=49.73, lon=7.33, r=8, n=10):
    """Show nearby devices."""
    if not (lon and lat and r):
        print("Missing arguments lon/lat.")

    print('Your location: {: 7.4f}, {:8.4f}'.format(lat, lon))
    print('Search radius: {}\n'.format(format_distance(r)))

    try:
        devices = show_nearby_devices(lat, lon, r, n)
    except NoResultFound:
        print('(No devices nearby) \n\nYou may want to increase the search radius r.')
    else:
        print('{:^11} | {:^18} | {}'.format('ogn address', 'Location', 'distance / bearing'))
        print('{:-<11} | {:-<18} | {:-<18}'.format('', '', ''))
        for device in devices:

            print("{:>11} | {: 7.4f}, {:8.4f} | {:>10}   {:>2}".format(
                device['device']['ogn_address'],
                device['device']['location']['lat'],
                device['device']['location']['lon'],
                format_distance(device['distance']),
                format_fuzzy_direction(device['direction'])))
