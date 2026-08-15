#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
