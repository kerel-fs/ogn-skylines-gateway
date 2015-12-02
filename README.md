# OGN Skylines Gateway
This application forwards packets from the [OpenGliderNetwork](http://glidernet.org) to [Skylines](https://skylines.aero).

## Installation and Setup
0. Update git-submodule `ogn-python`
```
$ git submodule init
$ git submodule update
```

1. Install python requirements
```
pip install -r requirements.txt
```

2. Create database
```
$ ./manage.py db.init
```

3. Insert some data into the database
```
$ ./manage.py db.insert "DD1234" "DEADBEEF"
```

## Running the server
Start the gateway with the follwing command.

```
$ ./manage.py run --logfile 'ogn-skylines.log'
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
    init                   Initialize the database.
    insert                 Insert a new user into the database.
```

## License
Licensed under the [AGPLv3](LICENSE) or any later version.

## Author
Fabian P. Schmidt, <kerel-fs@gmx.de>

## Contact
- via email
- via IRC: `kerel` on [freenode](irc://chat.freenode.net)
            related channels: `#skylines` and `#glidernet` on freenode
