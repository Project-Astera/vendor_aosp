import os
import json
import sys

# Get the codename from command-line arguments
if len(sys.argv) != 2:
    print("Usage: python vendor/aosp/tools/get_official_maintainer.py <codename>")
    sys.exit(1)

codename_to_check = sys.argv[1]

# Get GitHub PAT from the environment variable
github_pat = os.environ.get("GITHUB_PAT")

if github_pat is None:
    print("GitHub Personal Access Token (GITHUB_PAT) not set.")
    sys.exit(1)

try:
    url = "https://raw.githubusercontent.com/Project-Astera-Devices/devices/thurisu/devices.json"

    # Conditional import for Python 2.x and 3.x
    try:
        from urllib.request import Request, urlopen, HTTPError
    except ImportError:
        from urllib2 import Request, urlopen, HTTPError

    headers = {"Authorization": "token {}".format(github_pat)}
    req = Request(url, headers=headers)

    # Open the URL and read the JSON response
    if sys.version_info.major == 2:
        try:
            response = urlopen(req, timeout=10)
            data = json.loads(response.read().decode("utf-8"))
        except HTTPError as http_error:
            print("unknown - check your GITHUB_PAT var")
            sys.exit(1)
        except ValueError as e:
            print("unknown - check your GITHUB_PAT var")
            sys.exit(1)
    else:
        import requests
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print("unknown - check your GITHUB_PAT var")
            sys.exit(1)

    for res in data:
        if res['codename'] == codename_to_check:
            for version in res['supported_versions']:
                if version['version_code'] == 'thurisu':
                    print(res['maintainer'])
                    sys.exit(0)
except Exception as e:
    if isinstance(e, HTTPError):
        print("Error:", e)
        sys.exit(1)
    else:
        print("Error:", e)

print("unknown")