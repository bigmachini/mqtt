def connect_to_wifi_and_update():
    import time, machine, network, gc
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from main.ota_updater import OTAUpdater
    import main.secrets as secret

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secret.WIFI_SSID, secret.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/bigmachini/mqtt', main_dir='main', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del (otaUpdater)
        gc.collect()


def start_app():
    import main.main as main
    main.start()
    # import main.home_automation as home_auto
    # home_auto.start()


connect_to_wifi_and_update()
start_app()
