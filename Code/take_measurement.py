from relay_code import relay_setup, turn_off
from Prova_210_serial_comm import cycle_autoscan


if __name__ == "__main__":
    print("===================================")
    print("Starting PV measurement")
    print("===================================")

    try:
        # Initialise GPIO and relay system
        relay_setup()

        # Measure Channel 1 and Channel 2 once each
        cycle_autoscan(num_scans=1)

        print("===================================")
        print("Measurement completed successfully")
        print("===================================")

    except Exception as e:
        print("===================================")
        print("MEASUREMENT ERROR:")
        print(e)
        print("===================================")

    finally:
        # Disconnect all PV modules from the PROVA
        turn_off()
        print("All relays switched OFF")
