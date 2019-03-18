import sys, os, base64, datetime, hashlib, hmac 
import requests
import sensor_lib as sl

service = 'execute-api'
host = 'ar0appcjs4.execute-api.us-east-2.amazonaws.com'
region = 'us-east-2'
endpoint = 'https://' + host
content_type = 'application/json'

# Auth keys configured in environment
access_key = ''
secret_key = ''
x_api_key = ''


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def check_keys():
    global access_key, secret_key, x_api_key

    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    x_api_key = os.environ.get('AWS_API_KEY')
    if access_key is None or secret_key is None or x_api_key is None:
        sl.handle_error('rest', 'REST keys not set')
 
def get_auth_header(canonical_request, date_stamp, x_amz_date, signed_headers):
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  x_amz_date + '\n' + credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    signing_key = get_signature_key(secret_key, date_stamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
    auth_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
    return auth_header;


# Main entry point:
#
# stage = beta | prod
# rest_api_uri = /temp | /regen | /salt
# method = POST | GET
# payload_body = JSON payload, e.g. {"date": "2019-02-14", "time": "20:15", "celcius": 8.456}
#
def consume_rest_api(stage, rest_api_uri, method, payload_body):
    check_keys()

    canonical_uri = '/' + stage + '/' + rest_api_uri
    payload_hash = hashlib.sha256(payload_body.encode('utf-8')).hexdigest()

    t = datetime.datetime.utcnow()
    x_amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')

    canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + x_amz_date + '\n' + 'x-api-key:' + x_api_key + '\n'
    signed_headers = 'content-type;host;x-amz-date;x-api-key'

    canonical_request = method + '\n' + canonical_uri + '\n\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    authorization_header = get_auth_header(canonical_request, date_stamp, x_amz_date, signed_headers);

    headers = {'Content-Type':content_type,
               'x-amz-date':x_amz_date, 
               'Authorization':authorization_header,
               'x-api-key':x_api_key}

    request_url = endpoint  + canonical_uri

    if (method == 'POST'):
        sl.write_to_file('rest', method + ' : ' + request_url , 'csv')
        r = requests.post(request_url, data=payload_body, headers=headers)
        msg = 'HTTP Status: ' + str(r.status_code) + ' : ' + r.text
        sl.write_to_file('rest', msg , 'csv')
    else:
        sl.handle_error('rest', 'Unsupported method: ' + method)

