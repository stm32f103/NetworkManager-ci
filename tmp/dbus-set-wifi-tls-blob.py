#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2011 Red Hat, Inc.
#

import dbus
import sys


def path_to_value(path):
    if sys.version_info[0] == 3:
        array = bytearray("file://" + path + "\0", "utf-8")
    else:
        array = "file://" + path + "\0"
    return dbus.ByteArray(array)


s_con = dbus.Dictionary(
    {
        "type": "802-11-wireless",
        "uuid": "7371bb78-c1f7-42a3-a9db-5b9566e8ca07",
        "id": "wifi-wlan0",
    }
)

if sys.version_info[0] == 3:
    homewifi = bytearray("homewifi", "utf-8")
else:
    homewifi = "homewifi"

s_wifi = dbus.Dictionary(
    {"ssid": dbus.ByteArray(homewifi), "security": "802-11-wireless-security"}
)

s_wsec = dbus.Dictionary({"key-mgmt": "wpa-eap"})

if sys.version_info[0] == 3:
    blob = bytearray(
        "3082045e30820346a003020102020900f7fca8c6f8a83c65300d06092a864886f70d0101050500307c310b3009060355040613025553311630140603550408130d4d6173736163687573657474733111300f0603550407130857657374666f726431163014060355040a130d526564204861742c20496e632e3118301606092a864886f70d010901160969744069742e636f6d3110300e0603550403130765617074657374301e170d3134303831323139313831345a170d3234303830393139313831345a307c310b3009060355040613025553311630140603550408130d4d6173736163687573657474733111300f0603550407130857657374666f726431163014060355040a130d526564204861742c20496e632e3118301606092a864886f70d010901160969744069742e636f6d3110300e060355040313076561707465737430820122300d06092a864886f70d01010105000382010f003082010a0282010100cd75107f35832c3ccfabe178c820c8254490c362bfab967d27da797a4c35b3c8670abdb1d9c200d030753a87c7ed8a1359d9aadae8d6e3a53d33ceb8c6ca2dd1908d46954807511d8f43a7cc7f1b24f99a16616cf47ea52cd8040dd6bc4c6f122f3e6ebc95eab6181c30bba29477e4b97dec4762af6c17dd64b305f8cbca0b547e55a494fb30640187b0e49936f2b8d049042b5f660023a2aec7f373c362e4ac32042791f255df2e9069d5fd8cd6b238ea1f66ba58be2511cb962477ce3ea26dd7772850d4cdfdbf0d849d9004cb30a67818911ddca41e547ea997e9efea98b1ff5b33f98f8cef4cb23534c96be067db365ae032d5340dc3316de832350ea3a70203010001a381e23081df301d0603551d0e041604147da094c586135233c83e9a0981eb98748a7ed9cb3081af0603551d230481a73081a480147da094c586135233c83e9a0981eb98748a7ed9cba18180a47e307c310b3009060355040613025553311630140603550408130d4d6173736163687573657474733111300f0603550407130857657374666f726431163014060355040a130d526564204861742c20496e632e3118301606092a864886f70d010901160969744069742e636f6d3110300e0603550403130765617074657374820900f7fca8c6f8a83c65300c0603551d13040530030101ff300d06092a864886f70d01010505000382010100b4ee7cd0c609f7189702d827babe5e2b040b1d850edd7fc5a8be2451c4173f8b4b0267c08a2184b246679a013e322eb8bc2fd6d3494275086e8da41ad4f977c2dbba92f1c9796d1d6a31f2108bed1e38545ca533681ed95fc7ef0daa8ac33cfc2654786ae0ce7a3f30685140d740e4f23d5fd768c40b4b35cde38fd79f90716b0ab29c6239647546634a806cce2b4bd735a473d296e909ad9eef73d75e386503ae8921512b355a012c4931f61bc4a6e713068514e91ce145d7bf1239f245d67d4b510a54a2a5bef972e2fbc7c48e9ff25f0af418e70252cb19413bb5f2fee741e3492339116241d80642bf6c4d2d1c7023dae0be7482df88bb8d04d6e96feab2",
        "utf-8",
    )
else:
    blob = "3082045e30820346a003020102020900f7fca8c6f8a83c65300d06092a864886f70d0101050500307c310b3009060355040613025553311630140603550408130d4d6173736163687573657474733111300f0603550407130857657374666f726431163014060355040a130d526564204861742c20496e632e3118301606092a864886f70d010901160969744069742e636f6d3110300e0603550403130765617074657374301e170d3134303831323139313831345a170d3234303830393139313831345a307c310b3009060355040613025553311630140603550408130d4d6173736163687573657474733111300f0603550407130857657374666f726431163014060355040a130d526564204861742c20496e632e3118301606092a864886f70d010901160969744069742e636f6d3110300e060355040313076561707465737430820122300d06092a864886f70d01010105000382010f003082010a0282010100cd75107f35832c3ccfabe178c820c8254490c362bfab967d27da797a4c35b3c8670abdb1d9c200d030753a87c7ed8a1359d9aadae8d6e3a53d33ceb8c6ca2dd1908d46954807511d8f43a7cc7f1b24f99a16616cf47ea52cd8040dd6bc4c6f122f3e6ebc95eab6181c30bba29477e4b97dec4762af6c17dd64b305f8cbca0b547e55a494fb30640187b0e49936f2b8d049042b5f660023a2aec7f373c362e4ac32042791f255df2e9069d5fd8cd6b238ea1f66ba58be2511cb962477ce3ea26dd7772850d4cdfdbf0d849d9004cb30a67818911ddca41e547ea997e9efea98b1ff5b33f98f8cef4cb23534c96be067db365ae032d5340dc3316de832350ea3a70203010001a381e23081df301d0603551d0e041604147da094c586135233c83e9a0981eb98748a7ed9cb3081af0603551d230481a73081a480147da094c586135233c83e9a0981eb98748a7ed9cba18180a47e307c310b3009060355040613025553311630140603550408130d4d6173736163687573657474733111300f0603550407130857657374666f726431163014060355040a130d526564204861742c20496e632e3118301606092a864886f70d010901160969744069742e636f6d3110300e0603550403130765617074657374820900f7fca8c6f8a83c65300c0603551d13040530030101ff300d06092a864886f70d01010505000382010100b4ee7cd0c609f7189702d827babe5e2b040b1d850edd7fc5a8be2451c4173f8b4b0267c08a2184b246679a013e322eb8bc2fd6d3494275086e8da41ad4f977c2dbba92f1c9796d1d6a31f2108bed1e38545ca533681ed95fc7ef0daa8ac33cfc2654786ae0ce7a3f30685140d740e4f23d5fd768c40b4b35cde38fd79f90716b0ab29c6239647546634a806cce2b4bd735a473d296e909ad9eef73d75e386503ae8921512b355a012c4931f61bc4a6e713068514e91ce145d7bf1239f245d67d4b510a54a2a5bef972e2fbc7c48e9ff25f0af418e70252cb19413bb5f2fee741e3492339116241d80642bf6c4d2d1c7023dae0be7482df88bb8d04d6e96feab2"

s_8021x = dbus.Dictionary(
    {
        "eap": ["tls"],
        "identity": "Bill Smith",
        "client-cert": dbus.ByteArray(blob),
        "ca-cert": path_to_value("/some/place/ca-cert.pem"),
        "private-key": dbus.ByteArray(blob),
        "private-key-password": "12345testing",
    }
)

s_ip4 = dbus.Dictionary({"method": "auto"})
s_ip6 = dbus.Dictionary({"method": "ignore"})

con = dbus.Dictionary(
    {
        "connection": s_con,
        "802-11-wireless": s_wifi,
        "802-11-wireless-security": s_wsec,
        "802-1x": s_8021x,
        "ipv4": s_ip4,
        "ipv6": s_ip6,
    }
)


bus = dbus.SystemBus()

proxy = bus.get_object(
    "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings"
)
settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

if sys.argv[1] == "Unsaved":
    settings.AddConnectionUnsaved(con)
if sys.argv[1] == "Saved":
    settings.AddConnection(con)
