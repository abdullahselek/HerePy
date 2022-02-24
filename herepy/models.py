import json


class HEREModel(object):
    """ Base class from which all here models will inherit."""

    def __init__(self, **kwargs):
        self.param_defaults = {}

    def __str__(self):
        """Returns a string representation of HEREModel. By default
        this is the same as as_json_string()."""
        return self.as_json_string()

    def __eq__(self, other):
        return other and self.as_dict() == other.as_dict()

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_json_string(self):
        """Returns the HEREModel as a JSON string based on key/value
        pairs returned from the as_dict() method."""
        return json.dumps(self.as_dict(), sort_keys=True)

    def as_dict(self):
        """Create a dictionary representation of the object. Please see inline
        comments on construction when dictionaries contain HEREModels."""
        data = {}

        for (key, value) in self.param_defaults.items():

            # If the value is a list, we need to create a list to hold the
            # dicts created by an object supporting the as_dict() method,
            # i.e., if it inherits from HEREModel. If the item in the list
            # doesn't support the as_dict() method, then we assign the value
            # directly. An example being a list of Media objects contained
            # within a Status object.
            if isinstance(getattr(self, key, None), (list, tuple, set)):
                data[key] = list()
                for subobj in getattr(self, key, None):
                    if getattr(subobj, "as_dict", None):
                        data[key].append(subobj.as_dict())
                    else:
                        data[key].append(subobj)

            # Not a list, *but still a subclass of HEREModel* and
            # and we can assign the data[key] directly with the as_dict()
            # method of the object. An example being a Status object contained
            # within a User object.
            elif getattr(getattr(self, key, None), "as_dict", None):
                data[key] = getattr(self, key).as_dict()

            # If the value doesn't have an as_dict() method, i.e., it's not
            # something that subclasses HEREModel, then we can use direct
            # assigment.
            elif getattr(self, key, None):
                data[key] = getattr(self, key, None)
        return data

    @classmethod
    def new_from_jsondict(cls, data, **kwargs):
        """Create a new instance based on a JSON dict. Any kwargs should be
        supplied by the inherited, calling class.

        Args:
            data (dict):
              A JSON dict, as converted from the JSON in the here API.
        """

        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val

        c = cls(**json_data)
        c._json = data
        return c


class GeocoderResponse(HEREModel):
    """A class representing the Geocoder Api response data."""

    def __init__(self, **kwargs):
        super(GeocoderResponse, self).__init__()
        self.param_defaults = {"items": None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class GeocoderReverseResponse(HEREModel):
    """A class representing the Geocoder Reverse Api response data."""

    def __init__(self, **kwargs):
        super(GeocoderReverseResponse, self).__init__()
        self.param_defaults = {"items": None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class RoutingResponse(HEREModel):
    """A class representing the Routing Api response data."""

    def __init__(self, **kwargs):
        super(RoutingResponse, self).__init__()
        self.param_defaults = {"response": None, "route_short": None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class RoutingResponseV8(HEREModel):
    """A class representing the Routing Api v8 response data."""

    def __init__(self, **kwargs):
        super(RoutingResponseV8, self).__init__()
        self.param_defaults = {"routes": None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class RoutingMatrixResponse(HEREModel):
    """A class representing the Routing Api matrix response data."""

    def __init__(self, **kwargs):
        super(RoutingMatrixResponse, self).__init__()
        self.param_defaults = {
            "matrixId": None,
            "matrix": None,
            "regionDefinition": None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class GeocoderAutoCompleteResponse(HEREModel):
    """A class representing the Geocoder Autocomplete Api response data."""

    def __init__(self, **kwargs):
        super(GeocoderAutoCompleteResponse, self).__init__()
        self.param_defaults = {"items": None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class RmeResponse(HEREModel):
    """A class representing the RME (Route Matcher) Api response data."""

    def __init__(self, **kwargs):
        super(RmeResponse, self).__init__()
        self.param_defaults = {"RouteLinks": [], "TracePoints": [], "Warnings": []}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class PlacesResponse(HEREModel):
    """A class representing the Places (Search) Api response data."""

    def __init__(self, **kwargs):
        super(PlacesResponse, self).__init__()
        self.param_defaults = {"items": None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class PublicTransitResponse(HEREModel):
    """A class representing the Public Transit Api response data."""

    def __init__(self, **kwargs):
        super(PublicTransitResponse, self).__init__()
        self.param_defaults = {"Res": None}

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class TrafficIncidentResponse(HEREModel):
    """A class representing the Traffic Incidents response provided by Traffic Api."""

    def __init__(self, **kwargs):
        super(TrafficIncidentResponse, self).__init__()
        self.param_defaults = {
            "TIMESTAMP": None,
            "VERSION": None,
            "TRAFFIC_ITEMS": None,
            "EXTENDED_COUNTRY_CODE": None,
            "error": None
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class DestinationWeatherResponse(HEREModel):
    """A class representing the Weather Forecasts for DestinationWeather Api."""

    def __init__(self, param_defaults, **kwargs):
        super(DestinationWeatherResponse, self).__init__()
        self.param_defaults = param_defaults

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @classmethod
    def new_from_jsondict(cls, data, param_defaults, **kwargs):
        """Create a new instance based on a JSON dict. Any kwargs should be
        supplied by the inherited, calling class.

        Args:
            data (dict):
              A JSON dict, as converted from the JSON in the here API.
        """

        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val

        c = cls(param_defaults, **json_data)
        c._json = data
        return c


class EVChargingStationsResponse(HEREModel):
    """A class representing the EV Charging Stations response data."""

    def __init__(self, **kwargs):
        super(EVChargingStationsResponse, self).__init__()
        self.param_defaults = {
            "hasMore": False,
            "count": 0,
            "evStations": None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class WaypointSequenceResponse(HEREModel):
    """A class representing the Fleet Telematics Waypoint Sequence response data."""

    def __init__(self, **kwargs):
        super(WaypointSequenceResponse, self).__init__()
        self.param_defaults = {
            "results": None,
            "errors": None,
            "warnings": None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class TrafficFlowResponse(HEREModel):
    """A class representing the Traffic API Flow response data."""

    def __init__(self, **kwargs):
        super(TrafficFlowResponse, self).__init__()
        self.param_defaults = {
            "RWS": [],
            "error": None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class TrafficFlowAvailabilityResponse(HEREModel):
    """A class representing the Traffic API Flow availability response data."""

    def __init__(self, **kwargs):
        super(TrafficFlowAvailabilityResponse, self).__init__()
        self.param_defaults = {
            "Response": [],
            "error": None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class IsolineRoutingResponse(HEREModel):
    """A class representing the Isoline Routing API Flow response data."""

    def __init__(self, **kwargs):
        super(IsolineRoutingResponse, self).__init__()
        self.param_defaults = {
            "departure": None,
            "arrival": None,
            "isolines": [],
            "error": None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))
