
import requests
import traceback

def exception_test():
    resp = requests.get('https://www.neelnanda.io/cancer')
    resp.raise_for_status()

try:
    exception_test()
except Exception as e:
    traceback.print_exc()
