#!/usr/bin/env python

from enum import Enum


class RouteMode(Enum):
    """Modes which is used in routing api functions."""

    fastest = "fastest"
    shortest = "shortest"
    balanced = "balanced"
    bicycle = "bicycle"
    car = "car"
    car_hov = "carHOV"
    traffic_enabled = "traffic:enabled"
    traffic_disabled = "traffic:disabled"
    traffic_default = "traffic:default"
    enabled = "enabled"
    pedestrian = "pedestrian"
    publicTransport = "publicTransport"
    publicTransportTimeTable = "publicTransportTimeTable"
    truck = "truck"

    def __str__(self):
        return "%s" % self._value_


class MatrixSummaryAttribute(Enum):
    """Defines an attribute to be included in the route matrix entries"""

    travel_time = "traveltime"
    cost_factor = "costfactor"
    distance = "distance"
    route_id = "routeid"

    def __str__(self):
        return "%s" % self._value_


class PlacesCategory(Enum):
    """Categories which are used in places api functions."""

    accomodation = "accomodation"
    administrative_areas_buildings = "administrative-areas-buildings"
    airport = "airport"
    atm_bank_exchange = "atm-bank-exchange"
    coffee_tea = "coffee-tea"
    eat_drink = "eat-drink"
    going_out = "going-out"
    hospital_health_care_facility = "hospital-health-care-facility"
    leisure_outdoor = "leisure-outdoor"
    natural_geographical = "natural-geographical"
    petrol_station = "petrol-station"
    restaurant = "restaurant"
    snacks_fast_food = "snacks-fast-food"
    sights_museums = "sights-museums"
    shopping = "shopping"
    toilet_rest_area = "toilet-rest-area"
    transport = "transport"

    def __str__(self):
        return "%s" % self._value_


class PublicTransitSearchMethod(Enum):
    """Search methods used in public transit search function"""

    fuzzy = "fuzzy"
    strict = "strict"

    def __str__(self):
        return "%s" % self._value_


class PublicTransitRoutingMode(Enum):
    """Routing types used in public transit api"""

    schedule = "schedule"
    realtime = "realtime"

    def __str__(self):
        return "%s" % self._value_


class PublicTransitModeType(Enum):
    """Mode types used in public transit api"""

    high_speed_train = 0
    intercity_train = 1
    inter_regional_train = 2
    regional_train = 3
    city_train = 4
    bus = 5
    ferry = 6
    subway = 7
    light_rail = 8
    private_bus = 9
    inclined = 10
    aerial = 11
    bus_rapid = 12
    monorail = 13
    flight = 14
    walk = 20

    def __str__(self):
        return "%s" % self._value_


class WeatherProductType(Enum):
    """Identifis the type of report to obtain."""

    observation = "observation"
    forecast_7days = "forecast_7days"
    forecast_7days_simple = "forecast_7days_simple"
    forecast_hourly = "forecast_hourly"
    forecast_astronomy = "forecast_astronomy"
    alerts = "alerts"
    nws_alerts = "nws_alerts"

    def __str__(self):
        return "%s" % self._value_


class EVStationConnectorTypes(Enum):
    """Defines the current connector types supported by the EV Charging Stations API."""

    unspecified = 0
    other = 1
    unallowed = 2
    small_paddle_inductive = 3
    large_paddle_inductive = 4
    nema_5_15 = 5
    nema_5_20 = 6
    bs_546_3_pin = 7
    cee_7_5 = 8
    cee_7_4_schuko = 9
    cee_7_7 = 10
    bs_1363__is_401_411__ms_58 = 11
    si_32 = 12
    as_nzs_3112 = 13
    cpcs_ccc = 14
    iram_2073 = 15
    sev_1011__t13 = 16
    sev_1011__t15 = 17
    sev_1011__t23 = 18
    sev_1011__t25 = 19
    section_107_2_d1 = 20
    thailand_tis_166_2549 = 21
    cei_23_16__VII = 22
    south_african_15_a__250_v = 23
    iec_60906_1_3_pin = 24
    avcon_connector = 25
    tesla_connector_high_power_wall = 26
    tesla_connector_universal_mobile = 27
    tesla_connector_spare_mobile = 28
    jevs_g_105 = 29
    iec_62196_2_type_1 = 30
    iec_62196_2_type_2_mennekes = 31
    iec_62196_2_type_3c = 32
    iec_62196_3_type_1_combo = 33
    iec_62196_3_type_2_combo = 34
    iec_60309_industrial_p_n_e = 35
    iec_60309_industrial_3p_e_n = 36
    iec_60309_industrial_2p_e_ac = 37
    iec_60309_industrial_p_n_e_ceeplus = 38
    iec_60309_industrial_3p_n_e = 39
    better_place_plug = 40
    marechal_plug = 41
    domestic_plug_socket_type_j = 42
    tesla_connector = 43
    iec_61851_1 = 44
    iec_62196_2_type_2_sae_j1772 = 45
    iec_60309_industrial_2p_e_dc = 46
    i_type_as__nz_3112 = 47
    domestic_plug_socket_type_a = 48
    domestic_plug_socket_type_c = 49

    def __str__(self):
        return "%s" % self._value_


class MultiplePickupOfferType(Enum):
    """Defines types of Fleet Telematics Api's pickup offers."""

    pickup = "pickup"
    drop = "drop"

    def __str__(self):
        return "%s" % self._value_


class IncidentsCriticalityStr(Enum):
    """Defines an attribute to be included in the traffic incidents requests."""

    critical = "critical"
    major = "major"
    minor = "minor"
    lowImpact = "lowImpact"

    def __str__(self):
        return "%s" % self._value_


class IncidentsCriticalityInt(Enum):
    """Defines an attribute to be included in the traffic incidents requests."""

    critical = 0
    major = 1
    minor = 2
    lowImpact = 3

    def __int__(self):
        return self._value_


class FlowProximityAdditionalAttributes(Enum):
    """Defines an additional attribute to be included in the traffic flow requests."""

    functional_class = "fc"
    shape = "sh"

    def __str__(self):
        return "%s" % self._value_


class IsolineRoutingMode(Enum):
    """Defines an attribute which specifies optimization is applied during isoline calculation."""

    fast = "fast"
    short = "short"

    def __str__(self):
        return "%s" % self._value_


class IsolineRoutingTransportMode(Enum):
    """Mode of transport to be used for the calculation of the isolines."""

    car = "car"
    truck = "truck"
    pedastrian = "pedastrian"

    def __str__(self):
        return "%s" % self._value_


class IsolineRoutingOptimizationMode(Enum):
    """Mode of how isoline calculation is optimized."""

    quality = "quality"
    performance = "performance"
    balanced = "balanced"

    def __str__(self):
        return "%s" % self._value_


class IsolineRoutingRangeType(Enum):
    """Type of ranges how isoline calculation is optimized."""

    distance = "distance"
    time = "time"
    consumption = "consumption"

    def __str__(self):
        return "%s" % self._value_
