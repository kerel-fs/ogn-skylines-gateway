from flask import Flask
from flask_restful import Resource, Api, reqparse

from ognskylines.dbutils import session
from ognskylines.model.functions import insert_user, delete_user, show_user, show_nearby_devices, IntegrityError, NoResultFound


LIST_LIMIT = 10
app = Flask(__name__)
app.config['DEBUG'] = True


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


api = Api(app)


class DevicesResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=float, required=True, help='no latitude (float) given')
        parser.add_argument('lon', type=float, required=True, help='no longitude (float) given')
        parser.add_argument('r', type=float, required=True, help='no range (float) in km given')
        args = parser.parse_args()

        try:
            devices = show_nearby_devices(args['lat'], args['lon'], args['r'], LIST_LIMIT)
        except NoResultFound:
            return {'message': '(No devices nearby) You may want to increase the search radius r.'}, 400
        else:
            return devices, 200


class UserResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('skylines_key', type=str, required=True, help='no valid skylines_key given')
        parser.add_argument('ogn_address', type=str, required=True, help='no valid ogn_address given')
        args = parser.parse_args()

        try:
            user = insert_user(args.skylines_key, args.ogn_address)
        except ValueError as e:
            return {'message': 'Invalid input, {}'.format(e)}, 400
        except NoResultFound:
            return {'message': 'Device not in database (insert device to ddb.glidernet.org)'}, 400
        except IntegrityError:
            return {'message': 'User already in the database.'}, 400
        else:
            return user, 201

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('skylines_key', type=str, required=True, help='no valid skylines_key given')
        args = parser.parse_args()

        try:
            users = show_user(args.skylines_key)
        except ValueError as e:
            return {'message': 'Invalid input, {}'.format(e)}, 400
        except NoResultFound:
            return {'message': 'User not in database.'}, 400
        else:
            return users, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('skylines_key', type=str, required=True, help='no valid skylines_key given')
        args = parser.parse_args()

        try:
            users = delete_user(args.skylines_key)
        except ValueError as e:
            return {'message': 'Invalid input, {}'.format(e)}, 400
        except NoResultFound:
            return {'message': 'User not in database.'}, 400
        else:
            return {'message': 'Deleted users.', 'users': users}, 200


api.add_resource(DevicesResource, '/v1/devices')
api.add_resource(UserResource, '/v1/user')
