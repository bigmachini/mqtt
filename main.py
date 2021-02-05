def connectToWifiAndUpdate():
    import time, machine, network, gc
    time.sleep(1)
    print('Memory free', gc.mem_free())
    
    from main.ota_updater import OTAUpdater
    import main.secrets as secret
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/bigmachini/mqtt', main_dir='main', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def startApp():
    import main.main as main
    main.start()


connectToWifiAndUpdate()
startApp()