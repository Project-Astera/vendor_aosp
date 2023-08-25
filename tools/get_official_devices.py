import json
import os
import sys
try:
    # For python3
    import urllib.error
    import urllib.parse
    import urllib.request
except:
    # For python2
    import imp
    import urllib2
    import urlparse
    urllib = imp.new_module('urllib')
    urllib.error = urllib2
    urllib.parse = urlparse
    urllib.request = urllib2
try:
    # Get GitHub PAT from the environment variable
    github_pat = os.environ.get("GITHUB_PAT")
    if github_pat is None:
        print("GitHub Personal Access Token (GITHUB_PAT) not set.")
        sys.exit(1)

    url = "https://raw.githubusercontent.com/Project-Astera-Devices/devices/thundra/devices.json"
    
    headers = {"Authorization": "token {}".format(github_pat)}
    req = urllib.request.Request(url, headers=headers)
    
    response = urllib.request.urlopen(req, timeout=10)
    data = json.loads(response.read())
    for res in data:
        for version in res['supported_versions']:
            if version['version_code'] == 'thundra':
                print (res['codename'])
                break
except urllib.error.HTTPError as http_error:
    print("check your GITHUB_PAT var")
except ValueError as e:
    print("check your GITHUB_PAT var")
except Exception as e:
    print(e)
