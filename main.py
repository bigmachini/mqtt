import _thread
from machine import reset
from time import sleep


def connect_to_wifi_and_update():
    import time, network, gc
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
            sleep(1)
            count = count + 1
            # TODO make this a configuration
            if count >= 120:
                reset()
    else:
        import ntptime
        ntptime.settime()

    print('\nnetwork config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater(secret.GITHUB_URL, main_dir='main', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        reset()
    else:
        del (otaUpdater)
        gc.collect()


try:
    import main.main as main

    connect_to_wifi_and_update()
    _thread.start_new_thread(main.start, (connect_to_wifi_and_update,))
except Exception as ex:
    print('main:: ex --> ', ex)
    reset()
