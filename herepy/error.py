#!/usr/bin/env python


class HEREError(Exception):

    """Base class for HERE errors"""

    @property
    def message(self):
        """Returns the first argument used to construct this error."""
        return self.args[0]


class UnauthorizedError(HEREError):

    """Unauthorized Error Type.

    Indicates authentication failure, invalid credentials were supplied.
    """


class InvalidRequestError(HEREError):

    """Invalid Request Error Type.

    Indicates an invalid or missing parameter value in the request, for example value given for the product parameter does not exist.
    """
