from pynput.keyboard import Key, Controller
# pyserial
from serial import Serial
from serial.tools import list_ports
import threading

class IrListener():

    def __init__(self):
        super().__init__()
        self.__Velocidad_serial = 115200
        self.__timeout = 0.3        

    def __ListenerEvent(self):
        try:
            # parametro arduino linux
            #arduionoPort = next(list_ports.grep("USB2.0-Serial"))[0]
            arduionoPort = next(list_ports.grep("CH340"))[0]  # parametro arduino uno
            PuertoSerie = Serial(
                arduionoPort, self.__Velocidad_serial, timeout=self.__timeout)
            print(f'puerto COM={arduionoPort}, Arduino iniciado')
        except:
            print("Arduino desconectado, por favor conecte")
        finally:
            while True:
                try:
                    # value_=PuertoSerie.readline()
                    #value= value_.decode("utf-8","ignore")
                    value = PuertoSerie.readline()
                    if(value != b''):
                        self.__pressKey(value)
                    if(value.find(b"4C7") != -1):
                        break
                except:
                    print("error inesperado")
                    break

    def start(self):
        evetn = threading.Thread(name="evento1", target=self.__ListenerEvent)
        evetn.start()

    def __pressKey(self, value):
        keyboard = Controller()
        key = self.__decodeCom(value)
        if(key != None):
            keyboard.press(key)
            keyboard.release(key)

    def __decodeCom(self, value):
        # "ok"=0,"right"=1,"down"=2,"left"=3,"UP"=4,"view"=5,"stop"=6
        keys = (Key.enter, Key.right, Key.down,
                Key.left, Key.up, Key.f12, Key.esc)
        values = {b'1045C\r\n': 0, b'45C\r\n': 0,
                  b'1045B\r\n': 1, b'45B\r\n': 1,
                  b'10459\r\n': 2, b'459\r\n': 2,
                  b'1045A\r\n': 3, b'45A\r\n': 3,
                  b'10458\r\n': 4, b'458\r\n': 4,
                  b'1042C\r\n': 5, b'42C\r\n': 5,
                  b'10431\r\n': 6, b'431\r\n': 6}
        if(value in values):
            return keys[values[value]]
        else:
            return None