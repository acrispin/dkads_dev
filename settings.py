from os import path

settings = dict(
            template_path = path.join(path.dirname(__file__), 'templates'),
            static_path = path.join(path.dirname(__file__), 'static'),
            xsrf_cookie = True,
            debug = True,
            # cookie_secret = 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
            cookie_secret = 'Hd7wOkBMR9axVHHuGKPs9udeNfvT8ETJhZvZ3m9RMTk=',
            login_url = "/auth/login/"
        )


# https://gist.github.com/didip/823887
# generate cookie_secret
"""
#!/usr/bin/env python

import base64
import uuid
 
print base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
print str(uuid.uuid4())

"""