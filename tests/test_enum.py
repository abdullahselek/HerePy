#!/usr/bin/env python

import unittest
import herepy
import sys

from enum import Enum


class RouteModeTest(unittest.TestCase):
    def test_valueofenum(self):
        fastest = herepy.RouteMode.fastest
        self.assertEqual(fastest.__str__(), "fastest")
        shortest = herepy.RouteMode.shortest
        self.assertEqual(shortest.__str__(), "shortest")
        balanced = herepy.RouteMode.balanced
        self.assertEqual(balanced.__str__(), "balanced")
        car = herepy.RouteMode.car
        self.assertEqual(car.__str__(), "car")
        car_hov = herepy.RouteMode.car_hov
        self.assertEqual(car_hov.__str__(), "carHOV")
        traffic_disabled = herepy.RouteMode.traffic_disabled
        self.assertEqual(traffic_disabled.__str__(), "traffic:disabled")
        enabled = herepy.RouteMode.enabled
        self.assertEqual(enabled.__str__(), "enabled")
        pedestrian = herepy.RouteMode.pedestrian
        self.assertEqual(pedestrian.__str__(), "pedestrian")
        publicTransport = herepy.RouteMode.publicTransport
        self.assertEqual(publicTransport.__str__(), "publicTransport")
        truck = herepy.RouteMode.truck
        self.assertEqual(truck.__str__(), "truck")
        traffic_default = herepy.RouteMode.traffic_default
        self.assertEqual(traffic_default.__str__(), "traffic:default")
        traffic_enabled = herepy.RouteMode.traffic_enabled
        self.assertEqual(traffic_enabled.__str__(), "traffic:enabled")


class PlacesCategoryTest(unittest.TestCase):
    def test_valueofenum(self):
        accomodation = herepy.PlacesCategory.accomodation
        self.assertEqual(accomodation.__str__(), "accomodation")


class PublicTransitSearchMethodTest(unittest.TestCase):
    def test_valueofenum(self):
        fuzzy = herepy.PublicTransitSearchMethod.fuzzy
        self.assertEqual(fuzzy.__str__(), "fuzzy")
        strict = herepy.PublicTransitSearchMethod.strict
        self.assertEqual(strict.__str__(), "strict")


class PublicTransitModeTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        high_speed_train = herepy.PublicTransitModeType.high_speed_train
        self.assertEqual(high_speed_train.__str__(), "0")
        intercity_train = herepy.PublicTransitModeType.intercity_train
        self.assertEqual(intercity_train.__str__(), "1")
        inter_regional_train = herepy.PublicTransitModeType.inter_regional_train
        self.assertEqual(inter_regional_train.__str__(), "2")
        regional_train = herepy.PublicTransitModeType.regional_train
        self.assertEqual(regional_train.__str__(), "3")
        city_train = herepy.PublicTransitModeType.city_train
        self.assertEqual(city_train.__str__(), "4")
        bus = herepy.PublicTransitModeType.bus
        self.assertEqual(bus.__str__(), "5")
        ferry = herepy.PublicTransitModeType.ferry
        self.assertEqual(ferry.__str__(), "6")
        subway = herepy.PublicTransitModeType.subway
        self.assertEqual(subway.__str__(), "7")
        light_rail = herepy.PublicTransitModeType.light_rail
        self.assertEqual(light_rail.__str__(), "8")
        private_bus = herepy.PublicTransitModeType.private_bus
        self.assertEqual(private_bus.__str__(), "9")
        inclined = herepy.PublicTransitModeType.inclined
        self.assertEqual(inclined.__str__(), "10")
        aerial = herepy.PublicTransitModeType.aerial
        self.assertEqual(aerial.__str__(), "11")
        bus_rapid = herepy.PublicTransitModeType.bus_rapid
        self.assertEqual(bus_rapid.__str__(), "12")
        monorail = herepy.PublicTransitModeType.monorail
        self.assertEqual(monorail.__str__(), "13")
        flight = herepy.PublicTransitModeType.flight
        self.assertEqual(flight.__str__(), "14")
        walk = herepy.PublicTransitModeType.walk
        self.assertEqual(walk.__str__(), "20")


class PublicTransitRoutingModeTest(unittest.TestCase):
    def test_valueofenum(self):
        schedule = herepy.PublicTransitRoutingMode.schedule
        self.assertEqual(schedule.__str__(), "schedule")
        realtime = herepy.PublicTransitRoutingMode.realtime
        self.assertEqual(realtime.__str__(), "realtime")


class EVStationConnectorTypesTest(unittest.TestCase):
    def test_valueofenum(self):
        unspecified = herepy.EVStationConnectorTypes.unspecified
        self.assertEqual(unspecified.__str__(), "0")
        other = herepy.EVStationConnectorTypes.other
        self.assertEqual(other.__str__(), "1")
        unallowed = herepy.EVStationConnectorTypes.unallowed
        self.assertEqual(unallowed.__str__(), "2")
        small_paddle_inductive = herepy.EVStationConnectorTypes.small_paddle_inductive
        self.assertEqual(small_paddle_inductive.__str__(), "3")
        large_paddle_inductive = herepy.EVStationConnectorTypes.large_paddle_inductive
        self.assertEqual(large_paddle_inductive.__str__(), "4")
        nema_5_15 = herepy.EVStationConnectorTypes.nema_5_15
        self.assertEqual(nema_5_15.__str__(), "5")
        nema_5_20 = herepy.EVStationConnectorTypes.nema_5_20
        self.assertEqual(nema_5_20.__str__(), "6")
        bs_546_3_pin = herepy.EVStationConnectorTypes.bs_546_3_pin
        self.assertEqual(bs_546_3_pin.__str__(), "7")
        cee_7_5 = herepy.EVStationConnectorTypes.cee_7_5
        self.assertEqual(cee_7_5.__str__(), "8")
        cee_7_4_schuko = herepy.EVStationConnectorTypes.cee_7_4_schuko
        self.assertEqual(cee_7_4_schuko.__str__(), "9")
        cee_7_7 = herepy.EVStationConnectorTypes.cee_7_7
        self.assertEqual(cee_7_7.__str__(), "10")

        bs_1363__is_401_411__ms_58 = (
            herepy.EVStationConnectorTypes.bs_1363__is_401_411__ms_58
        )
        self.assertEqual(bs_1363__is_401_411__ms_58.__str__(), "11")
        si_32 = herepy.EVStationConnectorTypes.si_32
        self.assertEqual(si_32.__str__(), "12")
        as_nzs_3112 = herepy.EVStationConnectorTypes.as_nzs_3112
        self.assertEqual(as_nzs_3112.__str__(), "13")
        cpcs_ccc = herepy.EVStationConnectorTypes.cpcs_ccc
        self.assertEqual(cpcs_ccc.__str__(), "14")
        iram_2073 = herepy.EVStationConnectorTypes.iram_2073
        self.assertEqual(iram_2073.__str__(), "15")
        sev_1011__t13 = herepy.EVStationConnectorTypes.sev_1011__t13
        self.assertEqual(sev_1011__t13.__str__(), "16")
        sev_1011__t15 = herepy.EVStationConnectorTypes.sev_1011__t15
        self.assertEqual(sev_1011__t15.__str__(), "17")
        sev_1011__t23 = herepy.EVStationConnectorTypes.sev_1011__t23
        self.assertEqual(sev_1011__t23.__str__(), "18")
        sev_1011__t25 = herepy.EVStationConnectorTypes.sev_1011__t25
        self.assertEqual(sev_1011__t25.__str__(), "19")
        section_107_2_d1 = herepy.EVStationConnectorTypes.section_107_2_d1
        self.assertEqual(section_107_2_d1.__str__(), "20")

        thailand_tis_166_2549 = herepy.EVStationConnectorTypes.thailand_tis_166_2549
        self.assertEqual(thailand_tis_166_2549.__str__(), "21")
        cei_23_16__VII = herepy.EVStationConnectorTypes.cei_23_16__VII
        self.assertEqual(cei_23_16__VII.__str__(), "22")
        south_african_15_a__250_v = (
            herepy.EVStationConnectorTypes.south_african_15_a__250_v
        )
        self.assertEqual(south_african_15_a__250_v.__str__(), "23")
        iec_60906_1_3_pin = herepy.EVStationConnectorTypes.iec_60906_1_3_pin
        self.assertEqual(iec_60906_1_3_pin.__str__(), "24")
        avcon_connector = herepy.EVStationConnectorTypes.avcon_connector
        self.assertEqual(avcon_connector.__str__(), "25")
        tesla_connector_high_power_wall = (
            herepy.EVStationConnectorTypes.tesla_connector_high_power_wall
        )
        self.assertEqual(tesla_connector_high_power_wall.__str__(), "26")
        tesla_connector_universal_mobile = (
            herepy.EVStationConnectorTypes.tesla_connector_universal_mobile
        )
        self.assertEqual(tesla_connector_universal_mobile.__str__(), "27")
        tesla_connector_spare_mobile = (
            herepy.EVStationConnectorTypes.tesla_connector_spare_mobile
        )
        self.assertEqual(tesla_connector_spare_mobile.__str__(), "28")
        jevs_g_105 = herepy.EVStationConnectorTypes.jevs_g_105
        self.assertEqual(jevs_g_105.__str__(), "29")
        iec_62196_2_type_1 = herepy.EVStationConnectorTypes.iec_62196_2_type_1
        self.assertEqual(iec_62196_2_type_1.__str__(), "30")

        iec_62196_2_type_2_mennekes = (
            herepy.EVStationConnectorTypes.iec_62196_2_type_2_mennekes
        )
        self.assertEqual(iec_62196_2_type_2_mennekes.__str__(), "31")
        iec_62196_2_type_3c = herepy.EVStationConnectorTypes.iec_62196_2_type_3c
        self.assertEqual(iec_62196_2_type_3c.__str__(), "32")
        iec_62196_3_type_1_combo = (
            herepy.EVStationConnectorTypes.iec_62196_3_type_1_combo
        )
        self.assertEqual(iec_62196_3_type_1_combo.__str__(), "33")
        iec_62196_3_type_2_combo = (
            herepy.EVStationConnectorTypes.iec_62196_3_type_2_combo
        )
        self.assertEqual(iec_62196_3_type_2_combo.__str__(), "34")
        iec_60309_industrial_p_n_e = (
            herepy.EVStationConnectorTypes.iec_60309_industrial_p_n_e
        )
        self.assertEqual(iec_60309_industrial_p_n_e.__str__(), "35")
        iec_60309_industrial_3p_e_n = (
            herepy.EVStationConnectorTypes.iec_60309_industrial_3p_e_n
        )
        self.assertEqual(iec_60309_industrial_3p_e_n.__str__(), "36")
        iec_60309_industrial_2p_e_ac = (
            herepy.EVStationConnectorTypes.iec_60309_industrial_2p_e_ac
        )
        self.assertEqual(iec_60309_industrial_2p_e_ac.__str__(), "37")
        iec_60309_industrial_p_n_e_ceeplus = (
            herepy.EVStationConnectorTypes.iec_60309_industrial_p_n_e_ceeplus
        )
        self.assertEqual(iec_60309_industrial_p_n_e_ceeplus.__str__(), "38")
        iec_60309_industrial_3p_n_e = (
            herepy.EVStationConnectorTypes.iec_60309_industrial_3p_n_e
        )
        self.assertEqual(iec_60309_industrial_3p_n_e.__str__(), "39")
        better_place_plug = herepy.EVStationConnectorTypes.better_place_plug
        self.assertEqual(better_place_plug.__str__(), "40")

        marechal_plug = herepy.EVStationConnectorTypes.marechal_plug
        self.assertEqual(marechal_plug.__str__(), "41")
        domestic_plug_socket_type_j = (
            herepy.EVStationConnectorTypes.domestic_plug_socket_type_j
        )
        self.assertEqual(domestic_plug_socket_type_j.__str__(), "42")
        tesla_connector = herepy.EVStationConnectorTypes.tesla_connector
        self.assertEqual(tesla_connector.__str__(), "43")
        iec_61851_1 = herepy.EVStationConnectorTypes.iec_61851_1
        self.assertEqual(iec_61851_1.__str__(), "44")
        iec_62196_2_type_2_sae_j1772 = (
            herepy.EVStationConnectorTypes.iec_62196_2_type_2_sae_j1772
        )
        self.assertEqual(iec_62196_2_type_2_sae_j1772.__str__(), "45")
        iec_60309_industrial_2p_e_dc = (
            herepy.EVStationConnectorTypes.iec_60309_industrial_2p_e_dc
        )
        self.assertEqual(iec_60309_industrial_2p_e_dc.__str__(), "46")
        i_type_as__nz_3112 = herepy.EVStationConnectorTypes.i_type_as__nz_3112
        self.assertEqual(i_type_as__nz_3112.__str__(), "47")
        domestic_plug_socket_type_a = (
            herepy.EVStationConnectorTypes.domestic_plug_socket_type_a
        )
        self.assertEqual(domestic_plug_socket_type_a.__str__(), "48")
        domestic_plug_socket_type_c = (
            herepy.EVStationConnectorTypes.domestic_plug_socket_type_c
        )
        self.assertEqual(domestic_plug_socket_type_c.__str__(), "49")


class MultiplePickupOfferTypeTest(unittest.TestCase):
    def test_valueofenum(self):
        pickup = herepy.MultiplePickupOfferType.pickup
        self.assertEqual(pickup.__str__(), "pickup")
        drop = herepy.MultiplePickupOfferType.drop
        self.assertEqual(drop.__str__(), "drop")


class IncidentsCriticalityStrTest(unittest.TestCase):
    def test_valueofenum(self):
        critical = herepy.IncidentsCriticalityStr.critical
        self.assertEqual(critical.__str__(), "critical")
        major = herepy.IncidentsCriticalityStr.major
        self.assertEqual(major.__str__(), "major")
        minor = herepy.IncidentsCriticalityStr.minor
        self.assertEqual(minor.__str__(), "minor")
        lowImpact = herepy.IncidentsCriticalityStr.lowImpact
        self.assertEqual(lowImpact.__str__(), "lowImpact")


class IncidentsCriticalityIntTest(unittest.TestCase):
    def test_valueofenum(self):
        critical = herepy.IncidentsCriticalityInt.critical
        self.assertEqual(critical.__int__(), 0)
        major = herepy.IncidentsCriticalityInt.major
        self.assertEqual(major.__int__(), 1)
        minor = herepy.IncidentsCriticalityInt.minor
        self.assertEqual(minor.__int__(), 2)
        lowImpact = herepy.IncidentsCriticalityInt.lowImpact
        self.assertEqual(lowImpact.__int__(), 3)


class FlowProximityAdditionalAttributesTest(unittest.TestCase):
    def test_valueofenum(self):
        functional_class = herepy.FlowProximityAdditionalAttributes.functional_class
        self.assertEqual(functional_class.__str__(), "fc")
        shape = herepy.FlowProximityAdditionalAttributes.shape
        self.assertEqual(shape.__str__(), "sh")


class IsolineRoutingModeTest(unittest.TestCase):

    def test_valueofenum(self):
        fast = herepy.IsolineRoutingMode.fast
        self.assertEqual(fast.__str__(), "fast")
        short = herepy.IsolineRoutingMode.short
        self.assertEqual(short.__str__(), "short")


class IsolineRoutingTransportModeTest(unittest.TestCase):

    def test_valueofenum(self):
        car = herepy.IsolineRoutingTransportMode.car
        self.assertEqual(car.__str__(), "car")
        truck = herepy.IsolineRoutingTransportMode.truck
        self.assertEqual(truck.__str__(), "truck")
        pedastrian = herepy.IsolineRoutingTransportMode.pedastrian
        self.assertEqual(pedastrian.__str__(), "pedastrian")
