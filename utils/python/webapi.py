
import requests


def get_info_github_user():

    auth = ('setivolkylany', 'totheend7525')

    # response = requests.get('https://api.github.com/user', auth=auth)

    # data = response.json()

    # data['total_private_repos']
    # data['location']
    # data['owned_private_repos']
    # data['followers_url']
    # data['following']
    # data['followers']
    # data['public_repos']
    # data['email']
    # data['url']
    # data['following_url']
    # data['repos_url']
    # data['created_at']

    response = requests.get('https://api.github.com/user/following', auth=auth)

    if not response.ok:
        response.raise_for_status()

    response_data = response.json()
    for following_data in response_data:
        print('{login}: {repos_url}'.format(**following_data))
        # if k in ['name', 'language', 'private', 'fork', 'updated_at', 'description']:


get_info_github_user()
