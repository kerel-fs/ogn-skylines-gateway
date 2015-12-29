#!/usr/bin/env python3

from flask.ext.script import Server, Manager
from ognskylines.web.app import app


manager = Manager(app)
manager.add_command("runserver", Server('10.0.2.15'))


if __name__ == "__main__":
    manager.run()
