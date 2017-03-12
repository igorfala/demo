import hashlib, base64, hmac


def get_proxy_signature(query_dict, secret):
    """
    Calculate the signature of the given query dict as per Shopify's documentation for proxy requests.
    See: http://docs.shopify.com/api/tutorials/application-proxies#security
    """
    # Convert secret to byte array
    #secret = bytearray(secret, encoding='utf-8')
    # Sort and combine query parameters into a single string.
    sorted_params = ''
    for key in sorted(query_dict.keys()):
        v = query_dict[key]
        if isinstance(v, list):
             v = ",".join(query_dict[key])
        sorted_params += "{0}={1}".format(key, v)
    signature = hmac.new(secret.encode(), sorted_params.encode(), hashlib.sha256)
    return signature.hexdigest()


def proxy_signature_is_valid(query_dict, secret):
    """
    Return true if the calculated signature matches that present in the query string of the given request.
    """
    # Extract the signature we're going to verify. If no signature's present, the request is invalid.
    try:
        signature_to_verify = query_dict.pop('signature')
    except KeyError:
        return False

    calculated_signature = get_proxy_signature(query_dict, secret)
    # Try to use compare_digest() to reduce vulnerability to timing attacks.
    # If it's not available, just fall back to regular string comparison.
    try:
        return hmac.compare_digest(calculated_signature, signature_to_verify)
    except AttributeError:
        return calculated_signature == signature_to_verify
