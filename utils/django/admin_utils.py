

def listing_accounts_with_admin_url(accounts):
    """ """

    if not accounts:
        return None


def remove_url_from_admin_urls(urls, url_name):

    acceptable_urls = (
        'changelist',
        'add',
        'history',
        'delete',
        'change',
    )

    if url_name not in acceptable_urls:
        msg = 'Not acceptable the Django`s standart admin url name ({0})'.format(
            ', '.join(acceptable_urls)
        )
        raise ValueError(msg)

    for admin_url in urls:
        if admin_url.name is not None and admin_url.name.endswith(url_name):
            urls.remove(admin_url)
