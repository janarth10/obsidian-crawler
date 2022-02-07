from retrying import retry

@retry(stop_max_attempt_number=7)
def test_retry():
    raise Exception('exception msg')
    print('failing')

test_retry()
