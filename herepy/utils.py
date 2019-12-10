#!/usr/bin/env python

import zlib
import base64

from urllib.parse import (urlparse, urlunparse, urlencode)

from herepy.error import HEREError

class Utils(object):
    """Helper class for main api classes"""

    @staticmethod
    def encode_parameters(parameters):
        """Return a string in key=value&key=value form.
        Values of None are not included in the output string.
        Args:
          parameters (dict):
            dictionary of query parameters to be converted.
        Returns:
          A URL-encoded string in "key=value&key=value" form
        """
        if parameters is None:
            return None
        if not isinstance(parameters, dict):
            raise HEREError("`parameters` must be a dict.")
        else:
            return urlencode(dict((k, v) for k, v in parameters.items() if v is not None))

    @staticmethod
    def build_url(url, extra_params=None):
        """Builds a url with given parameters which will
        be used in requests.
        Args:
          url (str):
            base url.
          extra_params (dict):
            dictionary of query parameters.
        Returns:
          A encoded url ready for the request"""

        # Break url into constituent parts
        (scheme, netloc, path, params, query, fragment) = urlparse(url)

        # Add any additional query parameters to the query string
        params_length = len(extra_params)
        if extra_params and params_length > 0:
            extra_query = Utils.encode_parameters(extra_params)
            # Add it to the existing query
            if query:
                query += '&' + extra_query
            else:
                query = extra_query

        # Return the rebuilt URL
        return urlunparse((scheme, netloc, path, params, query, fragment))

    @staticmethod
    def get_zipped_base64(content):
        content_bytes = content.encode('utf-8')
        content_zipped = zlib.compress(content_bytes)
        return base64.b64encode(content_zipped).decode('utf-8')
