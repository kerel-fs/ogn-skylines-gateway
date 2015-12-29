# OGN Skylines Gateway
[![Build Status](https://travis-ci.org/kerel-fs/ogn-skylines-gateway.png?branch=master)](https://travis-ci.org/kerel-fs/ogn-skylines-gateway)
This application forwards packets from the [OpenGliderNetwork](http://glidernet.org) to [Skylines](https://skylines.aero).

## Installation and Setup (dev)
1. Create virtual maschine with vagrant
   ```
   vagrant up
   ```

3. Log in to the virtual maschine

   ```
   vagrant ssh
   ```

4. Initialize the database and import registered devices from the [DDB](https://ddb.glidernet.org)

   ```
   cd /vagrant
   ./manage.py db.init
   ./manage.py devices.import_ddb
   ```

5. Insert some data into the database

   ```
   ./manage.py users.insert "DEADBEEF" "DD1234"
   ```

## Running the server
Start the gateway with the follwing command.

```
./manage.py run --logfile 'ogn-skylines.log'
```

## manage.py - Usage
```
usage: manage.py [<namespace>.]<command> [<args>]

positional arguments:
  command     the command to run

optional arguments:
  -h, --help  show this help message and exit

available commands:
  run                      Run the ogn-->skylines gateway.

  [db]
    drop                   Drop all tables.
    init                   Initialize the database.

  [devices]
    import_ddb             Import registered devices from the DDB (discards all devices before import).
    show_all               Show all devices with known location.
    show_nearby            Show nearby devices.

  [users]
    delete                 Delete a user.
    insert                 Insert a new user.
    show                   Show a user.
    show_all               Show all users.
```

## API

### List nearby devices
```
GET /devices?lat=1.1&lon=2.2&r=100
```

Response:

```
[
    {
        "device": {
            "location": {
                "latitude": "float, decimal degrees",
                "longitude": "float, decimal degrees"
            },
            "ogn_address": "hexadecimal string, 3 bytes",
            "timestamp": "2016-01-01 00:00:01"
        },
        "direction": "float, angle in degrees",
        "distance": "float, distance in km"
    },
    ...
]
```

### Insert a new user
```
POST /user?skylines_key={skylines_key}&ogn_address={ogn_address}
```

### Show a user
```
GET /user?skylines_key={skylines_key}
```

Response:
```
[
    {
        "ogn_address": "hexadecimal string, 3 bytes",
        "skylines_key": "hexadecimal string, 4 bytes"
    },
    ...
]
```

### Delete a user
```
DELETE /user?skylines_key={skylines_key}
```

## License
Licensed under the [AGPLv3](LICENSE) or any later version.

## Author
Fabian P. Schmidt, <kerel-fs@gmx.de>

## Contact
- IRC: `kerel` on [freenode](https://freenode.net/),
  related channels: `#skylines` and `#glidernet` on freenode
- email
