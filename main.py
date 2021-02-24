import _thread


def connect_to_wifi_and_update():
    import time, machine, network, gc
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from main.ota_updater import OTAUpdater
    import main.secrets as secret

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        count = 0
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secret.WIFI_SSID, secret.WIFI_PASSWORD)
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(1)
            count = count + 1
            #TODO make this a configuration
            if count >= 120:
                machine.reset()
    else:
        import ntptime
        ntptime.settime()

    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater(secret.GITHUB_URL, main_dir='main', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del (otaUpdater)
        gc.collect()


def start_app():
    # TODO: Add functionality to increase sleep time and sevearity of
    # situation when exceptions occur
    import machine
    try:
        import main.main as main
        main.start(connect_to_wifi_and_update)
    except Exception as ex:
        print('start_app:: ex --> ', ex)
        machine.reset()


try:
    connect_to_wifi_and_update()
    _thread.start_new_thread(start_app, ())
except Exception as ex:
    import machine

    print('main:: ex --> ', ex)
    machine.reset()
