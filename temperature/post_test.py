#!/usr/bin/python


import sensor_modules.rest_lib as rl

# Good
rl.consume_rest_api('beta', 'temp', 'POST', '{"date": "2021-05-06", "time": "03:19", "celcius": 5.456}')

# Bad Requests
rl.consume_rest_api('beta', 'temp', 'POST', '{"monkey": "2019-02-14", "time": "20:15", "celcius": 9.456}')
rl.consume_rest_api('beta', 'temp', 'POST', '{"date": "2019-02-14", "monkey": "20:15", "celcius": 9.456}')
rl.consume_rest_api('beta', 'temp', 'POST', '{"date": "2019-02-14", "time": "20:15", "monkey": 9.456}')

# Invalid data
rl.consume_rest_api('beta', 'temp', 'POST', '{"date": "2019-99-14", "time": "20:15", "celcius": 9.456}')
rl.consume_rest_api('beta', 'temp', 'POST', '{"date": "2019-02-14", "time": "99:15", "celcius": 9.456}')
rl.consume_rest_api('beta', 'temp', 'POST', '{"date": "2019-02-14", "time": "20:15", "celcius": ALAN}')

# Invalid  method
rl.consume_rest_api('beta', 'temp', 'GET', '{"date": "2019-02-14", "time": "20:15", "celcius": 9.456}')

# Unknown rest api uri
rl.consume_rest_api('beta', 'unknown', 'POST', '{"date": "2019-02-14", "time": "20:15", "celcius": 9.456}')

# Unknown staging area
rl.consume_rest_api('bench', 'temp', 'POST', '{"date": "2019-02-14", "time": "20:15", "celcius": 9.456}')

