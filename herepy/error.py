#!/usr/bin/env python

class HEREError(Exception):
    
    """Base class for HERE errors"""

    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]
