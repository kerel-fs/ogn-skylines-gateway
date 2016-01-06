from ognskylines.model.functions import insert_user, delete_user, show_user, show_users, IntegrityError, NoResultFound

from manager import Manager
manager = Manager()


@manager.command
def insert(ogn_address, skylines_key, add_device='n'):
    """Insert a new user."""

    skylines_key = str(skylines_key)
    ogn_address = str(ogn_address)
    try:
        user = insert_user(skylines_key, ogn_address, add_device == 'y')
    except ValueError as e:
        print('Invalid input, {}'.format(e))
    except NoResultFound:
        print('Device not in database (insert device to ddb.glidernet.org)')
    except IntegrityError:
        print('User already in the database.')
    else:
        print('Added {}.'.format(user))


@manager.command
def delete(skylines_key):
    """Delete a user."""

    skylines_key = str(skylines_key)
    try:
        users = delete_user(skylines_key)
    except ValueError as e:
        print('Invalid input, {}'.format(e))
    except NoResultFound:
        print('User not in database.')
    else:
        print('Deleted users:')
        for user in users:
            print('- {}'.format(user))


@manager.command
def show(skylines_key):
    """Show a user."""

    skylines_key = str(skylines_key)
    try:
        users = show_user(skylines_key)
    except ValueError as e:
        print('Invalid input, {}'.format(e))
    except NoResultFound:
        print('User not in database.')
    else:
        for user in users:
            print('{}'.format(user))


@manager.command
def show_all():
    """Show all users."""

    try:
        users = show_users()
    except ValueError as e:
        print('Invalid input, {}'.format(e))
    except NoResultFound:
        print('No User in database.')
    else:
        print('{:^12} | {:^11}'.format('skylines key', 'ogn address'))
        print('{:-<12} | {:-<11}'.format('', ''))
        for user in users:
            print("{:<12X} | {}".format(
                user.skylines_key,
                user.ogn_address))
