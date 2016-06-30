 Feature: nmcli: team

    @1257195
    @add_default_team
    @team
    Scenario: nmcli - team - add default team
     * Open editor for a type "team"
     * Submit "set team.interface-name nm-team" in editor
     * Submit "set team.connection-name nm-team" in editor
     * Save in editor
     * Enter in editor
     * Quit editor
    #Then Prompt is not running
    Then "nm-team" is visible with command "sudo teamdctl nm-team state dump"


    @ifcfg_team_slave_device_type
    @team
    Scenario: nmcli - team - slave ifcfg devicetype
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
    Then "DEVICETYPE=TeamPort" is visible with command "grep TYPE /etc/sysconfig/network-scripts/ifcfg-team0.0"


    @nmcli_novice_mode_create_team
    @team
    Scenario: nmcli - team - novice - create team
     * Open wizard for adding new connection
     * Expect "Connection type"
     * Submit "team" in editor
     * Expect "There .* optional"
     * Submit "no" in editor
     * Dismiss IP configuration in editor
    Then "nm-team" is visible with command "sudo teamdctl nm-team state dump"


    @nmcli_novice_mode_create_team-slave_with_default_options
    @team_slaves
    @team
    Scenario: nmcli - team - novice - create team-slave with default options
     * Add connection type "team" named "team0" for device "nm-team"
     * Open wizard for adding new connection
     * Expect "Connection type"
     * Submit "team-slave" in editor
     * Expect "Interface name"
     * Submit "eth1" in editor
     * Expect "aster"
     * Submit "nm-team" in editor
     * Expect "There .* optional"
     * Submit "no" in editor
     * Bring "up" connection "team-slave-eth1"
    Then Check slave "eth1" in team "nm-team" is "up"


    @1257237
    @add_two_slaves_to_team
    @team_slaves
    @team
    Scenario: nmcli - team - add slaves
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Bring "up" connection "team0.0"
     * Bring "up" connection "team0.1"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"


    @add_team_master_via_uuid
    @team_slaves
    @team
    # bug verification for 1057494
    Scenario: nmcli - team - master via uuid
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "team0" on device "eth1" named "team0.0"
     * Bring "up" connection "team0.0"
    Then Check slave "eth1" in team "nm-team" is "up"


    @remove_all_slaves
    @team_slaves
    @team
    Scenario: nmcli - team - remove last slave
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Bring "up" connection "team0.0"
     * Delete connection "team0.0"
    Then Check slave "eth1" in team "nm-team" is "down"


    @rhbz1294728
    @ver+=1.1
    @team @restart @team_slaves
    @team_restart_persistence
    Scenario: nmcli - team - restart persistence
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     When "nm-team:connected:team0" is visible with command "nmcli -t -f DEVICE,STATE,CONNECTION device" in "20" seconds
     * Restart NM
     * Restart NM
     * Restart NM
     Then Check slave "eth2" in team "nm-team" is "up"
      And Check slave "eth1" in team "nm-team" is "up"
      And "team0" is visible with command "nmcli con show -a"
      And "team0.0" is visible with command "nmcli con show -a"
      And "team0.1" is visible with command "nmcli con show -a"


    @remove_one_slave
    @team_slaves
    @team
    Scenario: nmcli - team - remove a slave
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Bring "up" connection "team0.1"
     * Bring "up" connection "team0.0"
     * Delete connection "team0.1"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "down"



    @change_slave_type_and_master
    @team_slaves
    @team
    Scenario: nmcli - connection - slave-type and master settings
     * Add connection type "team" named "team0" for device "nm-team"
     * Add connection type "ethernet" named "team0.0" for device "eth1"
     * Open editor for connection "team0.0"
     * Set a property named "connection.slave-type" to "team" in editor
     * Set a property named "connection.master" to "nm-team" in editor
     * Submit "yes" in editor
     * Submit "verify fix" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0.0"
    Then Check slave "eth1" in team "nm-team" is "up"



    @remove_active_team_profile
    @team_slaves
    @team
    Scenario: nmcli - team - remove active team profile
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Bring "up" connection "team0.0"
    Then Check slave "eth1" in team "nm-team" is "up"
     * Delete connection "team0"
    Then Team "nm-team" is down


    @disconnect_active_team
    @team_slaves
    @team
    Scenario: nmcli - team - disconnect active team
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Bring "up" connection "team0"
     * Disconnect device "nm-team"
    Then Team "nm-team" is down


    @team_start_by_hand_no_slaves
    @team_slaves
    @team
    Scenario: nmcli - team - start team by hand with no slaves
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Disconnect device "nm-team"
     * Bring "down" connection "team0.0"
     * Bring "down" connection "team0.1"
    Then Team "nm-team" is down
     * Bring up connection "team0" ignoring error
    Then "nm-team" is visible with command "sudo teamdctl nm-team state dump"


    @rhbz1158529
    @team_slaves
    @team
    @team_slaves_start_via_master
    Scenario: nmcli - team - start slaves via master
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Disconnect device "nm-team"
     * Open editor for connection "team0"
     * Submit "set connection.autoconnect-slaves 1" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"


    @start_team_by_hand_all_auto
    @team_slaves
    @team
    Scenario: nmcli - team - start team by hand with all auto
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Disconnect device "nm-team"
     * Bring "down" connection "team0.0"
     * Bring "down" connection "team0.1"
    Then Team "nm-team" is down
     * Bring "up" connection "team0.0"
     * Bring "up" connection "team0.1"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"


    @team_activate
    @team_slaves
    @team
    Scenario: nmcli - team - activate
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Disconnect device "nm-team"
     * Bring "down" connection "team0.0"
     * Bring "down" connection "team0.1"
    Then Team "nm-team" is down
     * Open editor for connection "team0.0"
     * Submit "activate" in editor
     * Enter in editor
     * Save in editor
     * Quit editor
     * Execute "sleep 3"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "down"


    @start_team_by_hand_one_auto
    @veth
    @team_slaves
    @team
    Scenario: nmcli - team - start team by hand with one auto
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0.0"
     * Submit "set connection.autoconnect no" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0.0"
     * Bring "up" connection "team0.1"
     * Bring "up" connection "team0"
    Then Check slave "eth1" in team "nm-team" is "down"
    Then Check slave "eth2" in team "nm-team" is "up"


    @start_team_on_boot
    @veth
    @team_slaves
    @team
    Scenario: nmcli - team - start team on boot
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0"
     * Submit "set connection.autoconnect yes" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0.0"
     * Submit "set connection.autoconnect yes" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0.1"
     * Submit "set connection.autoconnect yes" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
     * Reboot
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"


    @team_start_on_boot_with_nothing_auto
    @veth
    @team_slaves
    @team
    Scenario: nmcli - team - start team on boot - nothing auto
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0.0"
     * Submit "set connection.autoconnect no" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0.1"
     * Submit "set connection.autoconnect no" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0"
     * Submit "set connection.autoconnect no" in editor
     * Save in editor
     * Quit editor
     #* Bring up connection "team0" ignoring error
     * Bring "up" connection "team0.0"
     * Bring "up" connection "team0.1"
     * Reboot
    Then Team "nm-team" is down


    #VVV    THIS IS DIFFERENT IN BOND AREA

    @team_start_on_boot_with_one_auto_only
    @veth
    @team_slaves
    @team
    Scenario: nmcli - team - start team on boot - one slave auto only
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0.0"
     * Submit "set connection.autoconnect no" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0.1"
     * Submit "set connection.autoconnect yes" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0"
     * Submit "set connection.autoconnect no" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
     * Bring "down" connection "team0"
     * Reboot
    Then Check slave "eth2" in team "nm-team" is "up"
    Then Check slave "eth1" in team "nm-team" is "down"


    @team_start_on_boot_with_team_and_one_slave_auto
    @veth
    @team_slaves
    @team
    Scenario: nmcli - team - start team on boot - team and one slave auto
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0.0"
     * Submit "set connection.autoconnect no" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0.1"
     * Submit "set connection.autoconnect yes" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0"
     * Submit "set connection.autoconnect yes" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
     * Reboot
    Then Check slave "eth2" in team "nm-team" is "up"
    Then Check slave "eth1" in team "nm-team" is "down"


    @config_loadbalance
    @team_slaves
    @team
    Scenario: nmcli - team - config - set loadbalance mode
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0"
     * Submit "set team.config {\\"device\\":\"nm-team\",\"runner\":{\"name\":\"loadbalance\"},\"ports\":{\"eth1\":{},\"eth2\": {}}}" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
     * Bring "up" connection "team0.1"
     * Bring "up" connection "team0.0"
    Then "\"kernel_team_mode_name\": \"loadbalance\"" is visible with command "sudo teamdctl nm-team state dump"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"


    # @config_lacp
    # @team_slaves
    # @team
    # Scenario: nmcli - team - config - set lacp mode
    #  * Add connection type "team" named "team0" for device "nm-team"
    #  * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
    #  * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
    #  * Open editor for connection "team0"
    #  * Submit "set team.config {"device":"nm-team","runner":{"name":"lacp","active":true,"fast_rate":true,"tx_hash":["eth","ipv4","ipv6"]},"link_watch":{"name": "ethtool"},"ports":{"eth1":{},"eth2":{}}}" in editor
    #  * Save in editor
    #  * Quit editor
    #  * Bring "up" connection "team0"
    #  #* Bring "up" connection "team0.0"
    #  #* Bring "up" connection "team0.1"
    # Then '"runner_name": "lacp"' is visible with command 'sudo teamdctl nm-team state dump'
    # Then Check slave "eth1" in team "nm-team" is "up"
    # Then Check slave "eth2" in team "nm-team" is "up"


    @config_broadcast
    @team_slaves
    @team
    Scenario: nmcli - team - config - set broadcast mode
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0"
     * Submit "set team.config {    \"device\":       \"nm-team\",  \"runner\":       {\"name": \"broadcast\"},  \"ports\":        {\"eth1\": {}, \"eth2\": {}}}" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
     * Bring "up" connection "team0.1"
     * Bring "up" connection "team0.0"
    Then "\"kernel_team_mode_name\": \"broadcast\"" is visible with command "sudo teamdctl nm-team state dump"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"



    @config_invalid
    @team_slaves
    @team
    @clean
    Scenario: nmcli - team - config - set invalid mode
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0"
     * Submit "set team.config {\"blah\":1,\"blah\":2,\"blah\":3}" in editor
     * Save in editor
     * Quit editor
     * Bring up connection "team0" ignoring error
    Then Team "nm-team" is down


    @rhbz1255927
    @team_slaves
    @team
    @team_set_mtu
    Scenario: nmcli - team - set mtu
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Open editor for connection "team0.0"
     * Set a property named "802-3-ethernet.mtu" to "9000" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0.1"
     * Set a property named "802-3-ethernet.mtu" to "9000" in editor
     * Save in editor
     * Quit editor
     * Open editor for connection "team0"
     * Set a property named "802-3-ethernet.mtu" to "9000" in editor
     * Set a property named "ipv4.method" to "manual" in editor
     * Set a property named "ipv4.addresses" to "1.1.1.2/24" in editor
     * Save in editor
     * Quit editor
     * Disconnect device "nm-team"
     * Bring "up" connection "team0"
     * Bring "up" connection "team0.1"
     * Bring "up" connection "team0.0"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"
    Then "mtu 9000" is visible with command "ip a s eth1 |grep mtu" in "25" seconds
    Then "mtu 9000" is visible with command "ip a s eth2 |grep mtu"
    Then "mtu 9000" is visible with command "ip a s nm-team |grep mtu"


    @remove_config
    @team_slaves
    @team
    Scenario: nmcli - team - config - remove
     * Add connection type "team" named "team0" for device "nm-team"
     * Add slave connection for master "nm-team" on device "eth1" named "team0.0"
     * Add slave connection for master "nm-team" on device "eth2" named "team0.1"
     * Bring "up" connection "team0.0"
     * Bring "up" connection "team0.1"
     * Open editor for connection "team0"
     * Submit "set team.config {\"device\":\"nm-team\",\"runner\":{\"name\":\"loadbalance\"},\"ports\":{\"eth1\":{},\"eth2\": {}}}" in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
     * Bring "up" connection "team0.0"
     * Bring "up" connection "team0.1"
    Then "\"kernel_team_mode_name\": \"loadbalance\"" is visible with command "sudo teamdctl nm-team state dump"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"
     * Open editor for connection "team0"
     * Submit "set team.config" in editor
     * Enter in editor
     * Save in editor
     * Quit editor
     * Bring "up" connection "team0"
     * Bring "up" connection "team0.1"
     * Bring "up" connection "team0.0"
    Then "\"kernel_team_mode_name\": \"loadbalance\"" is not visible with command "sudo teamdctl nm-team state dump"
    Then Check slave "eth1" in team "nm-team" is "up"
    Then Check slave "eth2" in team "nm-team" is "up"


    @ver-=1.1
    @dummy
    @teamd
    @team_reflect_changes_from_outside_of_NM
    Scenario: nmcli - team - reflect changes from outside of NM
    * Finish "systemd-run --unit teamd teamd --team-dev=team0"
    * Finish "sleep 2"
    When "team0\s+team\s+unmanaged" is visible with command "nmcli d"
    * Finish "ip link set dev team0 up"
    When "team0\s+team\s+disconnected" is visible with command "nmcli d"
    * Finish "ip link add dummy0 type dummy"
    * Finish "ip addr add 1.1.1.1/24 dev team0"
    When "team0\s+team\s+connected\s+team0" is visible with command "nmcli d" in "5" seconds
    When "dummy0\s+dummy\s+unmanaged" is visible with command "nmcli d"
    * Finish "teamdctl team0 port add dummy0"
    When "dummy0\s+dummy\s+connected\s+dummy" is visible with command "nmcli d"
    Then "TEAM.SLAVES:\s+dummy0" is visible with command "nmcli -f team.slaves dev show team0"


    @ver+=1.1.1
    @dummy
    @teamd
    @team_reflect_changes_from_outside_of_NM
    Scenario: nmcli - team - reflect changes from outside of NM
    * Finish "systemd-run --unit teamd teamd --team-dev=team0"
    * Finish "sleep 2"
    When "team0\s+team\s+unmanaged" is visible with command "nmcli d"
    * Finish "ip link set dev team0 up"
    When "team0\s+team\s+unmanaged" is visible with command "nmcli d"
    * Finish "ip link add dummy0 type dummy"
    * Finish "ip addr add 1.1.1.1/24 dev team0"
    When "team0\s+team\s+connected\s+team0" is visible with command "nmcli d" in "5" seconds
    When "dummy0\s+dummy\s+unmanaged" is visible with command "nmcli d"
    * Finish "teamdctl team0 port add dummy0"
    When "dummy0\s+dummy\s+connected\s+dummy" is visible with command "nmcli d"
    Then "TEAM.SLAVES:\s+dummy0" is visible with command "nmcli -f team.slaves dev show team0"


    @rhbz1145988
    @team_slaves
    @team
    @kill_teamd
    Scenario: NM - team - kill teamd
     * Add connection type "team" named "team0" for device "nm-team"
     * Execute "sleep 6"
     * Execute "killall -9 teamd; sleep 2"
    Then "teamd -o -n -U -D -N -t nm-team" is visible with command "ps aux|grep -v grep| grep teamd"


    @describe
    @team
    Scenario: nmcli - team - describe team
     * Open editor for a type "team"
     Then Check "<<< team >>>|=== \[config\] ===|\[NM property description\]" are present in describe output for object "team"
     Then Check "The JSON configuration for the team network interface.  The property should contain raw JSON configuration data suitable for teamd, because the value is passed directly to teamd. If not specified, the default configuration is used.  See man teamd.conf for the format details." are present in describe output for object "team.config"
      * Submit "g t" in editor
     Then Check "NM property description|The JSON configuration for the team network interface.  The property should contain raw JSON configuration data suitable for teamd, because the value is passed directly to teamd. If not specified, the default configuration is used.  See man teamd.conf for the format details." are present in describe output for object "config"
      * Submit "g c" in editor
     Then Check "The JSON configuration for the team network interface.  The property should contain raw JSON configuration data suitable for teamd, because the value is passed directly to teamd. If not specified, the default configuration is used.  See man teamd.conf for the format details." are present in describe output for object " "


    @rhbz1183444
    @veth
    @team
    @bridge
    @team_enslave_to_bridge
    Scenario: nmcli - team - enslave team device to bridge
     * Add a new connection of type "team" and options "con-name team0 autoconnect no ifname nm-team"
     * Add a new connection of type "bridge" and options "con-name br10 autoconnect no ifname bridge0 ip4 192.168.177.100/24 gw4 192.168.177.1"
     * Execute "nmcli connection modify id team0 connection.master bridge0 connection.slave-type bridge"
     * Bring "up" connection "team0"
    Then "bridge0:bridge:connected:br10" is visible with command "nmcli -t -f DEVICE,TYPE,STATE,CONNECTION device" in "5" seconds
    Then "nm-team:team:connected:team0" is visible with command "nmcli -t -f DEVICE,TYPE,STATE,CONNECTION device" in "5" seconds


    @rhbz1303968
    @team @bridge @team_slaves
    @team_in_bridge_mtu
    Scenario: nmcli - team - enslave team device to bridge and set mtu
     * Add a new connection of type "bridge" and options "con-name bridge0 autoconnect no ifname bridge0 -- 802-3-ethernet.mtu 9000 ipv4.method manual ipv4.addresses 192.168.177.100/24 ipv4.gateway 192.168.177.1"
     * Add a new connection of type "team" and options "con-name team0 autoconnect no ifname nm-team master bridge0 -- 802-3-ethernet.mtu 9000"
     * Add a new connection of type "ethernet" and options "con-name team0.0 autoconnect no ifname eth1 master nm-team -- 802-3-ethernet.mtu 9000"
     * Add a new connection of type "ethernet" and options "con-name team0.0 autoconnect no ifname eth1 master nm-team -- 802-3-ethernet.mtu 9000"
     * Bring "up" connection "bridge0"
     * Bring "up" connection "team0"
     * Bring "up" connection "team0.0"
     Then "mtu 9000" is visible with command "ip a s eth1"
     Then "mtu 9000" is visible with command "ip a s nm-team"
     Then "mtu 9000" is visible with command "ip a s bridge0"
