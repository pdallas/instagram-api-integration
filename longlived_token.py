from defines import getCreds, makeApiCall


def getLongLivedAccessToken(params):
    """ Get long lived access token

    	API Endpoint:
    		https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
    	Returns:
    		object: data from the endpoint
    	"""

    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['grant_type'] = 'fb_exchange_token'  # input token is the access token
    endpointParams['client_id'] = params['client_id']  # access token to get debug info on
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['fb_exchange_token'] = params['access_token']

    url = params['endpoint_base'] + 'oauth/access_token'
    return makeApiCall(url, endpointParams, params['debug'])


params = getCreds()
params['debug'] = 'no'
response = getLongLivedAccessToken(params)

print("\n ---- ACCESS TOKEN INFO ----\n")  # section header
print("Access Token:")  # label
print(response['json_data']['access_token'])  # display access token
