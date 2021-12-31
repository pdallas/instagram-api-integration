from defines import getCreds, makeApiCall


def getUserPages(params):
    """ Get facebook pages for a user

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}
    Returns:
        object: data from the endpoint
    """

    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['access_token'] = params['access_token']  # access token

    url = params['endpoint_base'] + 'me/accounts'  # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])  # make the api call


params = getCreds()  # get creds
params['debug'] = 'no'  # set debug
response = getUserPages(params)  # get debug info


def getAllPages():
    c = 0
    all_ids = []
    all_names = []
    for _ in response['json_data']['data']:
        all_names.append(response['json_data']['data'][c]['name'])
        all_ids.append(response['json_data']['data'][c]['id'])
        c = c + 1
    return all_ids

