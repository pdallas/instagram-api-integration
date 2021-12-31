from defines import getCreds, makeApiCall


# from get_insta_acc import getAll_ig_pages


# params = getCreds()  # get creds
# params['debug'] = 'yes'
# new = getAll_ig_pages()
# print(new)


def getStoryMediaId(params):
    """ Get facebook pages for a user

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{instagram-account-id}/stories
    Returns:
        object: data from the endpoint
    """

    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['access_token'] = params['access_token']  # access token
    endpointParams['instagram_account_id'] = params['instagram_account_id']
    url = params['endpoint_base'] + params['instagram_account_id'] + '/stories'  # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])  # make the api call


def getMediaInsights(params):
    """ Get insights for a specific media id

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}
    Returns:
        object: data from the endpoint
    """
    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['metric'] = 'exits,impressions,reach,replies,taps_forward,taps_back'
    endpointParams['access_token'] = params['access_token']  # access token

    url = params['endpoint_base'] + params['latest_media_id'] + '/insights'  # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])  # make the api call


def loops(ig_store):
    insightslist = []
    i = 0
    params = getCreds()  # get creds
    params['debug'] = 'yes'
    params['page_id'] = '105140544217695'  # users page id
    params['instagram_account_id'] = '17841406665384366'  # users instagram account id
    params['ig_username'] = ig_store  # ig username
    response = getStoryMediaId(params)
    params['latest_media_id'] = response['json_data']['data'][0]['id']
    response = getMediaInsights(params)

    for insight in response['json_data']['data']:  # loop over post insights
        if insight['name'] == 'exits':
            insightslist.append(insight['values'][0]['value'])
        if insight['name'] == 'impressions':
            insightslist.append(insight['values'][0]['value'])
        if insight['name'] == 'reach':
            insightslist.append(insight['values'][0]['value'])
        if insight['name'] == 'replies':
            insightslist.append(insight['values'][0]['value'])
        if insight['name'] == 'taps_forward':
            insightslist.append(insight['values'][0]['value'])
        if insight['name'] == 'taps_back':
            insightslist.append(insight['values'][0]['value'])

    # testing
    #f = open("../../thewebnir.txt", "a")
    #f.write(str(insightslist))
    #f.close()
    return insightslist



