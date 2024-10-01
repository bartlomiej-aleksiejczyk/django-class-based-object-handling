from django import template
from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def update_url(url, table_name, key, value):
    """
    Custom template tag to update the URL with a new parameter.
    Args:
        url (str): The current URL.
        table_name (str): The table name to namespace the parameter.
        key (str): The query parameter key to update.
        value (str): The new value for the query parameter.

    Returns:
        str: The updated URL.
    """
    print(url)

    scheme, netloc, path, query_string, fragment = urlsplit(url)

    query_params = dict(parse_qsl(query_string))

    namespaced_key = f"{table_name}__{key}"
    query_params[namespaced_key] = value

    updated_query_string = urlencode(query_params, doseq=True)
    return urlunsplit((scheme, netloc, path, updated_query_string, fragment))
