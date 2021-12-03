#Acoustic Modem Data class by Adrian Fernandez

#TODO: need to install bitarray library to make bit arrays -- DONE
#TODO: look into how adafruit's gps library works to know how to store it properly -- DONE 
#TODO: create a method that stores variabes onto a JSON File so data is easier to compare -- DONE
#TODO: Split json file into segments because of formating issues -- DONE

#Import Things to Note:
# - Make sure to install required libraries
#   - $ pip3 intall bitarray
#   - $ pip3 install adafruit_blinka
# - JSON dump() does not accept user defined objects, must convert object to some kind of string
# - JSON dump() does not format the file, must format some other way (link above)

class modemData:
    counter = 0 #Static counter variable to store number of objects are stored

    def __init__(self, _startTime: int, _endTime : int, _bitArr : str, _longitude : float = None, _latitude : float = None ):
        """
        Variable info for parameters:
        - startTime is the time the transmittion/receiving time began in ns                                                         | int
        - endTime is the time transmittion/receving ended in ns                                                                     | int
        - bitArr is to store the bit array                                                                                          | str
        - longitude is to store longitude from adafruit_gps from the gps unit of the Tx, Rx does not need to store                  | Assume it a float from Adafruit GPS object
        - latitude is to store latitude from adafruit_gps from the gps unit of the Tx, Rx does not need to store                    | Assume it a float from Adafruit GPS object
      
        Some other variable:
        - counter is a static variable that counts number of objects made                                                           | static int var
        - instance stores the current value of counter so we can number the output of the JSON value, can remove later if needed    | int var     
        """
        
        self.startTime = _startTime
        self.endTime = _endTime
        self.latitude = _latitude
        self.longitude = _longitude
        self.bitArr = _bitArr
        modemData.counter += 1
        self.instance = modemData.counter

    def storeJSON(self):
        
        #if else statement based on if it is Tx or Rx
        #convert variables into a dictionary to dump into a JSON file

        #Rx
        if self.latitude is None:
            info = {"No.": self.instance, "Receiving Began": self.startTime, "Receiving Ended":self.endTime, "Recieved Time Displacement":self.endTime - self.startTime, "Bit Array": (self.bitArr)}
            
        #Tx
        else:
            info = {"No.": self.instance, "Transmittion Began": self.startTime, "Transmittion Ended": self.endTime, "Sent Time Displacement":self.endTime - self.startTime, "Bit Array": (self.bitArr), "Latitude" : "{0:.6f} degrees".format(self.latitude), "Longitude": "{0:.6f} degrees".format(self.longitude)}
        '''
        print(info)
        dumpFile.write(f"{info}")
        dumpFile.write('\n')
        '''
        
        return info 

