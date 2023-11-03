from pyfingerprint.pyfingerprint import PyFingerprint

def enroll_fingerprint():
    try:
        # Initialize the fingerprint sensor
        fingerprint_sensor = PyFingerprint('/dev/ttyUSB0', 57600)
        if not fingerprint_sensor.verifyPassword():
            raise ValueError("The given fingerprint sensor password is incorrect!")

        print("Place your finger on the sensor...")

        while not fingerprint_sensor.readImage():
            pass
        
        fingerprint_sensor.convertImage(1)
        
        #print(fingerprint_sensor.getTemplateIndex(0))

        if fingerprint_sensor.storeTemplate(0): # change number each time
            print(f"Fingerprint successfully stored.")
        else:
            print("Error storing fingerprint template.")
        print(fingerprint_sensor.getTemplateCount())

    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    enroll_fingerprint()
