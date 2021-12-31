from defines import getCreds, makeApiCall
import json

def getUser(params):
    """ Get facebook pages for a user

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}
    Returns:
        object: data from the endpoint
    """

    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['access_token'] = params['access_token']  # access token
    endpointParams['fields'] = 'name,username,id,profile_picture_url,biography,follows_count,followers_count,' \
                               'media_count'
    url = params['endpoint_base'] + params['instagram_account_id']  # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])  # make the api call


params = getCreds()
params["debug"] = 'yes'
new = getUser(params)
