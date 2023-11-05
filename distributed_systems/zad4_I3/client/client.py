import sys, Ice
import Demo

def handle_exit(communicator, exit_code):
    communicator.destroy()
    exit(exit_code)

def main():
    communicator = Ice.initialize(sys.argv)
    properties = communicator.getProperties()
    endpoints = properties.getProperty("Demo.Endpoints")

    while True:
        inp = input(">>> ")
        if len(inp) == 0: continue
        split_inp = inp.split()
        if (split_inp[0] == "quit"):
            handle_exit(communicator, 0)
        elif (split_inp[0] == "fuws"):
            base = communicator.stringToProxy(f"singleton:{endpoints}")
            fuws = Demo.FUWSObjectPrx.checkedCast(base)
            if not fuws:
                print("Invalid proxy")
                continue
            value = fuws.incrementAndGet()
            print(f"Value after incrementing: {value}")
        elif (split_inp[0] == "ruws"):
            if len(split_inp) < 3:
                print("Expected 3 arguments")
                continue
            object_id = split_inp[1]
            base = communicator.stringToProxy(f"{object_id}:{endpoints}")
            try:
                ruws = Demo.RUWSObjectPrx.checkedCast(base)
                if not ruws:
                    print("Invalid proxy")
                    continue
                ruws.saveALotOfData(split_inp[2])
                print(f"Called `saveALotOfData` with {split_inp[2]}")
            except Ice.ObjectNotExistException:
                print("This object does not exist")
                continue
        elif (split_inp[0] == "fuwos"):
            if len(split_inp) < 4:
                print("Expected 4 arguments")
                continue
            object_id = split_inp[1]
            base = communicator.stringToProxy(f"{object_id}:{endpoints}")
            try:
                fuwos = Demo.FUWOSObjectPrx.checkedCast(base)
                if not fuwos:
                    print("Invalid proxy")
                    continue
                word = fuwos.concatWords(split_inp[2], split_inp[3])
                print(f"Concatenated word: {word}")
            except Ice.ObjectNotExistException:
                print("This object does not exist")
                continue
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
