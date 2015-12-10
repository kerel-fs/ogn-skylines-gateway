# OGN Skylines Gateway
[![Build Status](https://travis-ci.org/kerel-fs/ogn-skylines-gateway.png?branch=master)](https://travis-ci.org/kerel-fs/ogn-skylines-gateway)
This application forwards packets from the [OpenGliderNetwork](http://glidernet.org) to [Skylines](https://skylines.aero).

## Installation and Setup
0. Update git-submodule `ogn-python`

   ```
   git submodule init
   git submodule update
   ```

1. Install python requirements

   ```
   pip install -r requirements.txt
   ```

2. Create database

   ```
   ./manage.py db.init
   ```

3. Insert some data into the database

   ```
   ./manage.py db.insert "DD1234" "DEADBEEF"
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
    import_ddb             Import registered devices from the DDB (flushed the device list).
    init                   Initialize the database.
    insert                 Insert a new user into the database.
    show_all               Show all devices with known location.
    show_nearby            Show nearby devices.
```

## License
Licensed under the [AGPLv3](LICENSE) or any later version.

## Author
Fabian P. Schmidt, <kerel-fs@gmx.de>

## Contact
- IRC: `kerel` on [freenode](https://freenode.net/),
  related channels: `#skylines` and `#glidernet` on freenode
- email
