#!/usr/bin/env python

import sys
import unittest
from enum import Enum

from herepy import (AerialMapTileResourceType, AvoidFeature,
                    BaseMapTileResourceType, EVStationConnectorTypes,
                    FlowProximityAdditionalAttributes, IncidentsCriticalityInt,
                    IncidentsCriticalityStr, IsolineRoutingMode,
                    IsolineRoutingOptimizationMode, IsolineRoutingRangeType,
                    IsolineRoutingTransportMode, MapImageFormatType,
                    MapImageResourceType, MapTileApiType, MatrixRoutingMode,
                    MatrixRoutingProfile, MatrixRoutingTransportMode,
                    MatrixRoutingType, MatrixSummaryAttribute,
                    MultiplePickupOfferType, PlacesCategory,
                    PublicTransitModeType, PublicTransitRoutingMode,
                    PublicTransitSearchMethod, RouteMode,
                    RoutingApiReturnField, RoutingApiSpanField, RoutingMetric,
                    RoutingMode, RoutingTransportMode, ShippedHazardousGood,
                    TrafficMapTileResourceType, TruckType, TunnelCategory,
                    VectorMapTileLayer, WeatherProductType)


class RouteModeTest(unittest.TestCase):
    def test_valueofenum(self):
        fastest = RouteMode.fastest
        self.assertEqual(fastest.__str__(), "fastest")
        shortest = RouteMode.shortest
        self.assertEqual(shortest.__str__(), "shortest")
        balanced = RouteMode.balanced
        self.assertEqual(balanced.__str__(), "balanced")
        car = RouteMode.car
        self.assertEqual(car.__str__(), "car")
        car_hov = RouteMode.car_hov
        self.assertEqual(car_hov.__str__(), "carHOV")
        traffic_disabled = RouteMode.traffic_disabled
        self.assertEqual(traffic_disabled.__str__(), "traffic:disabled")
        enabled = RouteMode.enabled
        self.assertEqual(enabled.__str__(), "enabled")
        pedestrian = RouteMode.pedestrian
        self.assertEqual(pedestrian.__str__(), "pedestrian")
        publicTransport = RouteMode.publicTransport
        self.assertEqual(publicTransport.__str__(), "publicTransport")
        truck = RouteMode.truck
        self.assertEqual(truck.__str__(), "truck")
        traffic_default = RouteMode.traffic_default
        self.assertEqual(traffic_default.__str__(), "traffic:default")
        traffic_enabled = RouteMode.traffic_enabled
        self.assertEqual(traffic_enabled.__str__(), "traffic:enabled")


class PlacesCategoryTest(unittest.TestCase):
    def test_valueofenum(self):
        accomodation = PlacesCategory.accomodation
        self.assertEqual(accomodation.__str__(), "accomodation")


class PublicTransitSearchMethodTest(unittest.TestCase):
    def test_valueofenum(self):
        fuzzy = PublicTransitSearchMethod.fuzzy
        self.assertEqual(fuzzy.__str__(), "fuzzy")
        strict = PublicTransitSearchMethod.strict
        self.assertEqual(strict.__str__(), "strict")


class PublicTransitModeTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        high_speed_train = PublicTransitModeType.high_speed_train
        self.assertEqual(high_speed_train.__str__(), "0")
        intercity_train = PublicTransitModeType.intercity_train
        self.assertEqual(intercity_train.__str__(), "1")
        inter_regional_train = PublicTransitModeType.inter_regional_train
        self.assertEqual(inter_regional_train.__str__(), "2")
        regional_train = PublicTransitModeType.regional_train
        self.assertEqual(regional_train.__str__(), "3")
        city_train = PublicTransitModeType.city_train
        self.assertEqual(city_train.__str__(), "4")
        bus = PublicTransitModeType.bus
        self.assertEqual(bus.__str__(), "5")
        ferry = PublicTransitModeType.ferry
        self.assertEqual(ferry.__str__(), "6")
        subway = PublicTransitModeType.subway
        self.assertEqual(subway.__str__(), "7")
        light_rail = PublicTransitModeType.light_rail
        self.assertEqual(light_rail.__str__(), "8")
        private_bus = PublicTransitModeType.private_bus
        self.assertEqual(private_bus.__str__(), "9")
        inclined = PublicTransitModeType.inclined
        self.assertEqual(inclined.__str__(), "10")
        aerial = PublicTransitModeType.aerial
        self.assertEqual(aerial.__str__(), "11")
        bus_rapid = PublicTransitModeType.bus_rapid
        self.assertEqual(bus_rapid.__str__(), "12")
        monorail = PublicTransitModeType.monorail
        self.assertEqual(monorail.__str__(), "13")
        flight = PublicTransitModeType.flight
        self.assertEqual(flight.__str__(), "14")
        walk = PublicTransitModeType.walk
        self.assertEqual(walk.__str__(), "20")


class PublicTransitRoutingModeTest(unittest.TestCase):
    def test_valueofenum(self):
        schedule = PublicTransitRoutingMode.schedule
        self.assertEqual(schedule.__str__(), "schedule")
        realtime = PublicTransitRoutingMode.realtime
        self.assertEqual(realtime.__str__(), "realtime")


class EVStationConnectorTypesTest(unittest.TestCase):
    def test_valueofenum(self):
        unspecified = EVStationConnectorTypes.unspecified
        self.assertEqual(unspecified.__str__(), "0")
        other = EVStationConnectorTypes.other
        self.assertEqual(other.__str__(), "1")
        unallowed = EVStationConnectorTypes.unallowed
        self.assertEqual(unallowed.__str__(), "2")
        small_paddle_inductive = EVStationConnectorTypes.small_paddle_inductive
        self.assertEqual(small_paddle_inductive.__str__(), "3")
        large_paddle_inductive = EVStationConnectorTypes.large_paddle_inductive
        self.assertEqual(large_paddle_inductive.__str__(), "4")
        nema_5_15 = EVStationConnectorTypes.nema_5_15
        self.assertEqual(nema_5_15.__str__(), "5")
        nema_5_20 = EVStationConnectorTypes.nema_5_20
        self.assertEqual(nema_5_20.__str__(), "6")
        bs_546_3_pin = EVStationConnectorTypes.bs_546_3_pin
        self.assertEqual(bs_546_3_pin.__str__(), "7")
        cee_7_5 = EVStationConnectorTypes.cee_7_5
        self.assertEqual(cee_7_5.__str__(), "8")
        cee_7_4_schuko = EVStationConnectorTypes.cee_7_4_schuko
        self.assertEqual(cee_7_4_schuko.__str__(), "9")
        cee_7_7 = EVStationConnectorTypes.cee_7_7
        self.assertEqual(cee_7_7.__str__(), "10")

        bs_1363__is_401_411__ms_58 = EVStationConnectorTypes.bs_1363__is_401_411__ms_58
        self.assertEqual(bs_1363__is_401_411__ms_58.__str__(), "11")
        si_32 = EVStationConnectorTypes.si_32
        self.assertEqual(si_32.__str__(), "12")
        as_nzs_3112 = EVStationConnectorTypes.as_nzs_3112
        self.assertEqual(as_nzs_3112.__str__(), "13")
        cpcs_ccc = EVStationConnectorTypes.cpcs_ccc
        self.assertEqual(cpcs_ccc.__str__(), "14")
        iram_2073 = EVStationConnectorTypes.iram_2073
        self.assertEqual(iram_2073.__str__(), "15")
        sev_1011__t13 = EVStationConnectorTypes.sev_1011__t13
        self.assertEqual(sev_1011__t13.__str__(), "16")
        sev_1011__t15 = EVStationConnectorTypes.sev_1011__t15
        self.assertEqual(sev_1011__t15.__str__(), "17")
        sev_1011__t23 = EVStationConnectorTypes.sev_1011__t23
        self.assertEqual(sev_1011__t23.__str__(), "18")
        sev_1011__t25 = EVStationConnectorTypes.sev_1011__t25
        self.assertEqual(sev_1011__t25.__str__(), "19")
        section_107_2_d1 = EVStationConnectorTypes.section_107_2_d1
        self.assertEqual(section_107_2_d1.__str__(), "20")

        thailand_tis_166_2549 = EVStationConnectorTypes.thailand_tis_166_2549
        self.assertEqual(thailand_tis_166_2549.__str__(), "21")
        cei_23_16__VII = EVStationConnectorTypes.cei_23_16__VII
        self.assertEqual(cei_23_16__VII.__str__(), "22")
        south_african_15_a__250_v = EVStationConnectorTypes.south_african_15_a__250_v
        self.assertEqual(south_african_15_a__250_v.__str__(), "23")
        iec_60906_1_3_pin = EVStationConnectorTypes.iec_60906_1_3_pin
        self.assertEqual(iec_60906_1_3_pin.__str__(), "24")
        avcon_connector = EVStationConnectorTypes.avcon_connector
        self.assertEqual(avcon_connector.__str__(), "25")
        tesla_connector_high_power_wall = (
            EVStationConnectorTypes.tesla_connector_high_power_wall
        )
        self.assertEqual(tesla_connector_high_power_wall.__str__(), "26")
        tesla_connector_universal_mobile = (
            EVStationConnectorTypes.tesla_connector_universal_mobile
        )
        self.assertEqual(tesla_connector_universal_mobile.__str__(), "27")
        tesla_connector_spare_mobile = (
            EVStationConnectorTypes.tesla_connector_spare_mobile
        )
        self.assertEqual(tesla_connector_spare_mobile.__str__(), "28")
        jevs_g_105 = EVStationConnectorTypes.jevs_g_105
        self.assertEqual(jevs_g_105.__str__(), "29")
        iec_62196_2_type_1 = EVStationConnectorTypes.iec_62196_2_type_1
        self.assertEqual(iec_62196_2_type_1.__str__(), "30")

        iec_62196_2_type_2_mennekes = (
            EVStationConnectorTypes.iec_62196_2_type_2_mennekes
        )
        self.assertEqual(iec_62196_2_type_2_mennekes.__str__(), "31")
        iec_62196_2_type_3c = EVStationConnectorTypes.iec_62196_2_type_3c
        self.assertEqual(iec_62196_2_type_3c.__str__(), "32")
        iec_62196_3_type_1_combo = EVStationConnectorTypes.iec_62196_3_type_1_combo
        self.assertEqual(iec_62196_3_type_1_combo.__str__(), "33")
        iec_62196_3_type_2_combo = EVStationConnectorTypes.iec_62196_3_type_2_combo
        self.assertEqual(iec_62196_3_type_2_combo.__str__(), "34")
        iec_60309_industrial_p_n_e = EVStationConnectorTypes.iec_60309_industrial_p_n_e
        self.assertEqual(iec_60309_industrial_p_n_e.__str__(), "35")
        iec_60309_industrial_3p_e_n = (
            EVStationConnectorTypes.iec_60309_industrial_3p_e_n
        )
        self.assertEqual(iec_60309_industrial_3p_e_n.__str__(), "36")
        iec_60309_industrial_2p_e_ac = (
            EVStationConnectorTypes.iec_60309_industrial_2p_e_ac
        )
        self.assertEqual(iec_60309_industrial_2p_e_ac.__str__(), "37")
        iec_60309_industrial_p_n_e_ceeplus = (
            EVStationConnectorTypes.iec_60309_industrial_p_n_e_ceeplus
        )
        self.assertEqual(iec_60309_industrial_p_n_e_ceeplus.__str__(), "38")
        iec_60309_industrial_3p_n_e = (
            EVStationConnectorTypes.iec_60309_industrial_3p_n_e
        )
        self.assertEqual(iec_60309_industrial_3p_n_e.__str__(), "39")
        better_place_plug = EVStationConnectorTypes.better_place_plug
        self.assertEqual(better_place_plug.__str__(), "40")

        marechal_plug = EVStationConnectorTypes.marechal_plug
        self.assertEqual(marechal_plug.__str__(), "41")
        domestic_plug_socket_type_j = (
            EVStationConnectorTypes.domestic_plug_socket_type_j
        )
        self.assertEqual(domestic_plug_socket_type_j.__str__(), "42")
        tesla_connector = EVStationConnectorTypes.tesla_connector
        self.assertEqual(tesla_connector.__str__(), "43")
        iec_61851_1 = EVStationConnectorTypes.iec_61851_1
        self.assertEqual(iec_61851_1.__str__(), "44")
        iec_62196_2_type_2_sae_j1772 = (
            EVStationConnectorTypes.iec_62196_2_type_2_sae_j1772
        )
        self.assertEqual(iec_62196_2_type_2_sae_j1772.__str__(), "45")
        iec_60309_industrial_2p_e_dc = (
            EVStationConnectorTypes.iec_60309_industrial_2p_e_dc
        )
        self.assertEqual(iec_60309_industrial_2p_e_dc.__str__(), "46")
        i_type_as__nz_3112 = EVStationConnectorTypes.i_type_as__nz_3112
        self.assertEqual(i_type_as__nz_3112.__str__(), "47")
        domestic_plug_socket_type_a = (
            EVStationConnectorTypes.domestic_plug_socket_type_a
        )
        self.assertEqual(domestic_plug_socket_type_a.__str__(), "48")
        domestic_plug_socket_type_c = (
            EVStationConnectorTypes.domestic_plug_socket_type_c
        )
        self.assertEqual(domestic_plug_socket_type_c.__str__(), "49")


class MultiplePickupOfferTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        pickup = MultiplePickupOfferType.pickup
        self.assertEqual(pickup.__str__(), "pickup")
        drop = MultiplePickupOfferType.drop
        self.assertEqual(drop.__str__(), "drop")


class IncidentsCriticalityStrTest(unittest.TestCase):
    def test_valueofenum(self):
        critical = IncidentsCriticalityStr.critical
        self.assertEqual(critical.__str__(), "critical")
        major = IncidentsCriticalityStr.major
        self.assertEqual(major.__str__(), "major")
        minor = IncidentsCriticalityStr.minor
        self.assertEqual(minor.__str__(), "minor")
        lowImpact = IncidentsCriticalityStr.lowImpact
        self.assertEqual(lowImpact.__str__(), "lowImpact")


class IncidentsCriticalityIntTest(unittest.TestCase):
    def test_valueofenum(self):
        critical = IncidentsCriticalityInt.critical
        self.assertEqual(critical.__int__(), 0)
        major = IncidentsCriticalityInt.major
        self.assertEqual(major.__int__(), 1)
        minor = IncidentsCriticalityInt.minor
        self.assertEqual(minor.__int__(), 2)
        lowImpact = IncidentsCriticalityInt.lowImpact
        self.assertEqual(lowImpact.__int__(), 3)


class FlowProximityAdditionalAttributesTest(unittest.TestCase):
    def test_valueofenum(self):
        functional_class = FlowProximityAdditionalAttributes.functional_class
        self.assertEqual(functional_class.__str__(), "fc")
        shape = FlowProximityAdditionalAttributes.shape
        self.assertEqual(shape.__str__(), "sh")


class IsolineRoutingModeTest(unittest.TestCase):
    def test_valueofenum(self):
        fast = IsolineRoutingMode.fast
        self.assertEqual(fast.__str__(), "fast")
        short = IsolineRoutingMode.short
        self.assertEqual(short.__str__(), "short")


class IsolineRoutingTransportModeTest(unittest.TestCase):
    def test_valueofenum(self):
        car = IsolineRoutingTransportMode.car
        self.assertEqual(car.__str__(), "car")
        truck = IsolineRoutingTransportMode.truck
        self.assertEqual(truck.__str__(), "truck")
        pedestrian = IsolineRoutingTransportMode.pedestrian
        self.assertEqual(pedestrian.__str__(), "pedestrian")


class IsolineRoutingOptimizationModeTest(unittest.TestCase):
    def test_valueofenum(self):
        quality = IsolineRoutingOptimizationMode.quality
        self.assertEqual(quality.__str__(), "quality")
        performance = IsolineRoutingOptimizationMode.performance
        self.assertEqual(performance.__str__(), "performance")
        balanced = IsolineRoutingOptimizationMode.balanced
        self.assertEqual(balanced.__str__(), "balanced")


class IsolineRoutingRangeTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        distance = IsolineRoutingRangeType.distance
        self.assertEqual(distance.__str__(), "distance")
        time = IsolineRoutingRangeType.time
        self.assertEqual(time.__str__(), "time")
        consumption = IsolineRoutingRangeType.consumption
        self.assertEqual(consumption.__str__(), "consumption")


class MapTileApiTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        aerial = MapTileApiType.aerial
        self.assertEqual(aerial.__str__(), "aerial")
        base = MapTileApiType.base
        self.assertEqual(base.__str__(), "base")
        traffic = MapTileApiType.traffic
        self.assertEqual(traffic.__str__(), "traffic")


class BaseMapTileResourceTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        alabeltile = BaseMapTileResourceType.alabeltile
        self.assertEqual(alabeltile.__str__(), "alabeltile")
        basetile = BaseMapTileResourceType.basetile
        self.assertEqual(basetile.__str__(), "basetile")
        blinetile = BaseMapTileResourceType.blinetile
        self.assertEqual(blinetile.__str__(), "blinetile")
        labeltile = BaseMapTileResourceType.labeltile
        self.assertEqual(labeltile.__str__(), "labeltile")
        linetile = BaseMapTileResourceType.linetile
        self.assertEqual(linetile.__str__(), "linetile")
        lltile = BaseMapTileResourceType.lltile
        self.assertEqual(lltile.__str__(), "lltile")
        maptile = BaseMapTileResourceType.maptile
        self.assertEqual(maptile.__str__(), "maptile")
        streettile = BaseMapTileResourceType.streettile
        self.assertEqual(streettile.__str__(), "streettile")
        trucktile = BaseMapTileResourceType.trucktile
        self.assertEqual(trucktile.__str__(), "trucktile")
        truckonlytile = BaseMapTileResourceType.truckonlytile
        self.assertEqual(truckonlytile.__str__(), "truckonlytile")
        xbasetile = BaseMapTileResourceType.xbasetile
        self.assertEqual(xbasetile.__str__(), "xbasetile")
        trucknopttile = BaseMapTileResourceType.trucknopttile
        self.assertEqual(trucknopttile.__str__(), "trucknopttile")
        mapnopttile = BaseMapTileResourceType.mapnopttile
        self.assertEqual(mapnopttile.__str__(), "mapnopttile")


class AerialMapTileResourceTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        alabeltile = AerialMapTileResourceType.alabeltile
        self.assertEqual(alabeltile.__str__(), "alabeltile")
        basetile = AerialMapTileResourceType.basetile
        self.assertEqual(basetile.__str__(), "basetile")
        blinetile = AerialMapTileResourceType.blinetile
        self.assertEqual(blinetile.__str__(), "blinetile")
        labeltile = AerialMapTileResourceType.labeltile
        self.assertEqual(labeltile.__str__(), "labeltile")
        linetile = AerialMapTileResourceType.linetile
        self.assertEqual(linetile.__str__(), "linetile")
        lltile = AerialMapTileResourceType.lltile
        self.assertEqual(lltile.__str__(), "lltile")
        maptile = AerialMapTileResourceType.maptile
        self.assertEqual(maptile.__str__(), "maptile")
        streettile = AerialMapTileResourceType.streettile
        self.assertEqual(streettile.__str__(), "streettile")
        trucktile = AerialMapTileResourceType.trucktile
        self.assertEqual(trucktile.__str__(), "trucktile")
        truckonlytile = AerialMapTileResourceType.truckonlytile
        self.assertEqual(truckonlytile.__str__(), "truckonlytile")
        xbasetile = AerialMapTileResourceType.xbasetile
        self.assertEqual(xbasetile.__str__(), "xbasetile")
        trucknopttile = AerialMapTileResourceType.trucknopttile
        self.assertEqual(trucknopttile.__str__(), "trucknopttile")
        mapnopttile = AerialMapTileResourceType.mapnopttile
        self.assertEqual(mapnopttile.__str__(), "mapnopttile")


class TrafficMapTileResourceTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        flowbasetile = TrafficMapTileResourceType.flowbasetile
        self.assertEqual(flowbasetile.__str__(), "flowbasetile")
        flowlabeltile = TrafficMapTileResourceType.flowlabeltile
        self.assertEqual(flowlabeltile.__str__(), "flowlabeltile")
        flowtile = TrafficMapTileResourceType.flowtile
        self.assertEqual(flowtile.__str__(), "flowtile")
        traffictile = TrafficMapTileResourceType.traffictile
        self.assertEqual(traffictile.__str__(), "traffictile")


class VectorMapTileLayerTest(unittest.TestCase):
    def test_valueofenum(self):
        base = VectorMapTileLayer.base
        self.assertEqual(base.__str__(), "base")
        core = VectorMapTileLayer.core
        self.assertEqual(core.__str__(), "core")


class MapImageResourceTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        companylogo = MapImageResourceType.companylogo
        self.assertEqual(companylogo.__str__(), "companylogo")
        heat = MapImageResourceType.heat
        self.assertEqual(heat.__str__(), "heat")
        mapview = MapImageResourceType.mapview
        self.assertEqual(mapview.__str__(), "mapview")
        region = MapImageResourceType.region
        self.assertEqual(region.__str__(), "region")
        roadsign = MapImageResourceType.roadsign
        self.assertEqual(roadsign.__str__(), "roadsign")
        route = MapImageResourceType.route
        self.assertEqual(route.__str__(), "route")
        routing = MapImageResourceType.routing
        self.assertEqual(routing.__str__(), "routing")
        stat = MapImageResourceType.stat
        self.assertEqual(stat.__str__(), "stat")
        tiltmap = MapImageResourceType.tiltmap
        self.assertEqual(tiltmap.__str__(), "tiltmap")
        turnpoint = MapImageResourceType.turnpoint
        self.assertEqual(turnpoint.__str__(), "turnpoint")
        version = MapImageResourceType.version
        self.assertEqual(version.__str__(), "version")


class VectorMapTileLayerTest(unittest.TestCase):
    def test_valueofenum(self):
        base = VectorMapTileLayer.base
        self.assertEqual(base.__str__(), "base")
        core = VectorMapTileLayer.core
        self.assertEqual(core.__str__(), "core")


class MapImageFormatTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(MapImageFormatType.png._value_, 0)
        self.assertEqual(MapImageFormatType.jpeg._value_, 1)
        self.assertEqual(MapImageFormatType.gif._value_, 2)
        self.assertEqual(MapImageFormatType.bmp._value_, 3)
        self.assertEqual(MapImageFormatType.png8._value_, 4)
        self.assertEqual(MapImageFormatType.svg._value_, 5)


class MatrixRoutingTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(MatrixRoutingType.world.__str__(), "world")
        self.assertEqual(MatrixRoutingType.circle.__str__(), "circle")
        self.assertEqual(MatrixRoutingType.bounding_box.__str__(), "boundingBox")
        self.assertEqual(MatrixRoutingType.polygon.__str__(), "polygon")
        self.assertEqual(MatrixRoutingType.auto_circle.__str__(), "autoCircle")


class MatrixRoutingProfileTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(MatrixRoutingProfile.car_fast.__str__(), "carFast")
        self.assertEqual(MatrixRoutingProfile.car_short.__str__(), "carShort")
        self.assertEqual(MatrixRoutingProfile.truck_fast.__str__(), "truckFast")
        self.assertEqual(MatrixRoutingProfile.pedestrian.__str__(), "pedestrian")
        self.assertEqual(MatrixRoutingProfile.bicycle.__str__(), "bicycle")


class MatrixRoutingModeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(MatrixRoutingMode.fast.__str__(), "fast")
        self.assertEqual(MatrixRoutingMode.short.__str__(), "short")


class MatrixRoutingTransportModeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(MatrixRoutingTransportMode.car.__str__(), "car")
        self.assertEqual(MatrixRoutingTransportMode.truck.__str__(), "truck")
        self.assertEqual(MatrixRoutingTransportMode.pedestrian.__str__(), "pedestrian")
        self.assertEqual(MatrixRoutingTransportMode.bicycle.__str__(), "bicycle")


class MatrixSummaryAttributeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(MatrixSummaryAttribute.travel_times.__str__(), "travelTimes")
        self.assertEqual(MatrixSummaryAttribute.distances.__str__(), "distances")


class RoutingModeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(RoutingMode.fast.__str__(), "fast")
        self.assertEqual(RoutingMode.short.__str__(), "short")


class RoutingTransportModeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(RoutingTransportMode.car.__str__(), "car")
        self.assertEqual(RoutingTransportMode.truck.__str__(), "truck")
        self.assertEqual(RoutingTransportMode.pedestrian.__str__(), "pedestrian")
        self.assertEqual(RoutingTransportMode.bicycle.__str__(), "bicycle")
        self.assertEqual(RoutingTransportMode.scooter.__str__(), "scooter")
        self.assertEqual(RoutingTransportMode.taxi.__str__(), "taxi")
        self.assertEqual(RoutingTransportMode.bus.__str__(), "bus")


class RoutingMetricTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(RoutingMetric.metric.__str__(), "metric")
        self.assertEqual(RoutingMetric.imperial.__str__(), "imperial")


class RoutingApiReturnFieldTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(RoutingApiReturnField.polyline.__str__(), "polyline")
        self.assertEqual(RoutingApiReturnField.actions.__str__(), "actions")
        self.assertEqual(RoutingApiReturnField.instructions.__str__(), "instructions")
        self.assertEqual(RoutingApiReturnField.summary.__str__(), "summary")
        self.assertEqual(RoutingApiReturnField.travelSummary.__str__(), "travelSummary")
        self.assertEqual(
            RoutingApiReturnField.turnByTurnActions.__str__(), "turnByTurnActions"
        )
        self.assertEqual(RoutingApiReturnField.routeHandle.__str__(), "routeHandle")
        self.assertEqual(RoutingApiReturnField.passthrough.__str__(), "passthrough")
        self.assertEqual(RoutingApiReturnField.incidents.__str__(), "incidents")
        self.assertEqual(RoutingApiReturnField.routingZones.__str__(), "routingZones")


class RoutingApiSpanFieldTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(RoutingApiSpanField.walkAttributes.__str__(), "walkAttributes")
        self.assertEqual(
            RoutingApiSpanField.streetAttributes.__str__(), "streetAttributes"
        )
        self.assertEqual(RoutingApiSpanField.carAttributes.__str__(), "carAttributes")
        self.assertEqual(
            RoutingApiSpanField.truckAttributes.__str__(), "truckAttributes"
        )
        self.assertEqual(
            RoutingApiSpanField.scooterAttributes.__str__(), "scooterAttributes"
        )
        self.assertEqual(RoutingApiSpanField.names.__str__(), "names")
        self.assertEqual(RoutingApiSpanField.length.__str__(), "length")
        self.assertEqual(RoutingApiSpanField.duration.__str__(), "duration")
        self.assertEqual(RoutingApiSpanField.baseDuration.__str__(), "baseDuration")
        self.assertEqual(RoutingApiSpanField.countryCode.__str__(), "countryCode")
        self.assertEqual(
            RoutingApiSpanField.functionalClass.__str__(), "functionalClass"
        )
        self.assertEqual(RoutingApiSpanField.routeNumbers.__str__(), "routeNumbers")
        self.assertEqual(RoutingApiSpanField.speedLimit.__str__(), "speedLimit")
        self.assertEqual(RoutingApiSpanField.maxSpeed.__str__(), "maxSpeed")
        self.assertEqual(
            RoutingApiSpanField.dynamicSpeedInfo.__str__(), "dynamicSpeedInfo"
        )
        self.assertEqual(RoutingApiSpanField.segmentId.__str__(), "segmentId")
        self.assertEqual(RoutingApiSpanField.segmentRef.__str__(), "segmentRef")
        self.assertEqual(RoutingApiSpanField.consumption.__str__(), "consumption")
        self.assertEqual(RoutingApiSpanField.routingZones.__str__(), "routingZones")
        self.assertEqual(RoutingApiSpanField.notices.__str__(), "notices")


class AvoidFeatureTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(AvoidFeature.toll_road.__str__(), "tollRoad")
        self.assertEqual(
            AvoidFeature.controlled_access_highway.__str__(), "controlledAccessHighway"
        )
        self.assertEqual(AvoidFeature.ferry.__str__(), "ferry")
        self.assertEqual(AvoidFeature.tunnel.__str__(), "tunnel")
        self.assertEqual(AvoidFeature.dirt_road.__str__(), "dirtRoad")


class ShippedHazardousGoodTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(ShippedHazardousGood.explosive.__str__(), "explosive")
        self.assertEqual(ShippedHazardousGood.gas.__str__(), "gas")
        self.assertEqual(ShippedHazardousGood.flammable.__str__(), "flammable")
        self.assertEqual(ShippedHazardousGood.combustible.__str__(), "combustible")
        self.assertEqual(ShippedHazardousGood.organic.__str__(), "organic")
        self.assertEqual(ShippedHazardousGood.poison.__str__(), "poison")
        self.assertEqual(ShippedHazardousGood.radioactive.__str__(), "radioactive")
        self.assertEqual(ShippedHazardousGood.corrosive.__str__(), "corrosive")
        self.assertEqual(
            ShippedHazardousGood.poisonousInhalation.__str__(), "poisonousInhalation"
        )
        self.assertEqual(
            ShippedHazardousGood.harmfulToWater.__str__(), "harmfulToWater"
        )
        self.assertEqual(ShippedHazardousGood.other.__str__(), "other")


class TunnelCategoryTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(TunnelCategory.b.__str__(), "B")
        self.assertEqual(TunnelCategory.c.__str__(), "C")
        self.assertEqual(TunnelCategory.d.__str__(), "D")
        self.assertEqual(TunnelCategory.e.__str__(), "E")


class TruckTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        self.assertEqual(TruckType.straight.__str__(), "straight")
        self.assertEqual(TruckType.tractor.__str__(), "tractor")
