import json
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()


def tpe(string):
    keyboard.type(string)
    time.sleep(0.5)

def main():
    time.sleep(5)
    with open("data4.json", "r") as file:
        data = json.load(file)

    
    for key, value in data.items():
        tpe(key)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        for key2, value2 in value.items():
            for key3, value3 in value2.items():
                if key3 != "times":
                    value3 = int(value3)
                tpe(str(value3))
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
        


if __name__ == "__main__":
    main()