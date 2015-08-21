import time
import pytz
import datetime
import security
import subprocess
import simplejson

_tzperu = pytz.timezone("America/Lima")

# Utility functions
def run_cmd(command, inputdata=None, **kwargs):
    """Run command (with optional input) and return retcode/stdout/stderr"""
    default_kwargs = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    popen = subprocess.Popen(command, **dict(default_kwargs, **kwargs))
    outdata, errdata = popen.communicate(inputdata)
    return popen.returncode, outdata, errdata

def qtime():
    return datetime.datetime.now(_tzperu).strftime("%d %b, %H:%M %G")

def verify_password(clear_pwd, hashed_pwd):
    return security.pwd_context.verify(clear_pwd, hashed_pwd)

def pwgen():
    returncode, outdata, errdata = run_cmd(["pwgen", "-c", "-n", "-s", "-1"])
    assert returncode == 0
    return outdata.strip()
    
def custom_log(req):    
    return '%s - - [%s +0800] "%s %s %s" - - "%s" "%s"' % \
            (req.remote_ip, time.strftime("%d/%b/%Y:%X"), req.method, \
            req.uri, req.version, getattr(req, 'referer', '-'),req.headers['User-Agent'])

def getDictJsonFromCursor(cursor):
    array_rs = cursor.fetchall()
    columns = [column[0] for column in cursor.description]              
    results = [dict(zip(columns,row)) for row in array_rs]    
    array_json = simplejson.dumps(results)    
    return array_json

