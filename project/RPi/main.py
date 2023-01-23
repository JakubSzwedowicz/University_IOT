from .src.central_unit.central_unit import CentralUnit

def main():
    rpi = CentralUnit()
    rpi.run()

if __name__ == '__main__':
    main()
    