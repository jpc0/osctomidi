import platform
import os.path
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import mido
import yaml
import os
from threading import Lock

if not os.path.isfile('config.yaml'):
    os.system("python config.py")
    if not os.path.isfile('config.yaml'):
        print("Please rerun the application as set a midi output!")
        quit()


def edit_config(SysTrayIcon):
    global config
    global config_lock
    with config_lock:
        os.system("python config.py")
        config = get_config()


def exit_osctomidi(SysTrayIcon):
    os._exit(0)


def get_config():
    global config_lock
    with config_lock:
        stream = open('config.yaml', 'r')
        config = yaml.safe_load(stream)
        stream.close()
        return config


def check_config():
    config = get_config()
    if type(config) is not dict:
        os.system("python config.py")
        check_config()
    elif not "Selected Midi Output" in config.keys():
        os.system("python config.py")
        check_config()
    return config


config_lock = Lock()
config = check_config()


def pphandler(address, *args):
    global config_lock
    with config_lock:
        midi = mido.open_output(config["Selected Midi Output"])
    macros = []
    for i in args[0][0]:
        macros.append(str(i).strip())
    message = args[1]
    if message in macros:
        midimessage = mido.Message('note_on', note=29,
                                   channel=0, velocity=macros.index(message)+1)
        midi.send(midimessage)
        print("Midi note {note} sent with velocity {vel}".format(
            note=midimessage.note, vel=midimessage.velocity))
    midi.close()


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


def main():
    global config
    dispatcher = Dispatcher()
    dispatcher.map("/pp/*", pphandler, config['Macro List'])
    dispatcher.set_default_handler(default_handler)
    ip = "0.0.0.0"
    port = 3251
    server = ThreadingOSCUDPServer((ip, port), dispatcher)
    server.serve_forever()


if __name__ == "__main__":
    if platform.system() == "Windows":
        from infi.systray import SysTrayIcon
        menu_options = (("Config", None, edit_config),)
        with SysTrayIcon(
                None, "osctomidi", menu_options, on_quit=exit_osctomidi) as systray:
            main()
    else:
        main()
