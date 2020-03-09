# MotorDataReader 
# handles parsing .eng files and extracting data from them 
# also handles calculating the thrust and weight of the motor at any time using interpolation 
# somewhat accurate, the details of how http://www.thrustcurve.org calculates this information is not given
# TODO implement polynomial fitting curve to increase accuracy 

class MotorDataReader: 
    # constructor 
    def __init__(self,file):
        self.file = file
        self.parseFile() 
        self.computeStatistics() 

    
    # calculate the trust and weight of the motor at any given time 
    def getThrustWeight(self,time):
        #compute the thrust and weight of the motor at a given time 
        if(time > self.burnTime):
            #after burn... 
            return [0, self.motorDryWeight]
        elif(time < 0):
            #hmmmmmmmmmmmmmm
            return [0,self.motorTotalWeight]
        else:
            # estimate the thrust using linear interpolation, estimate the weight by the proportion of total impulse left in the system 
            # for thrust, find which points are in the middle 
            counter = 1 
            found = False
            thrust = 0 
            impulse = 0 
            # loop until a greater time stamp is found 
            while(found == False): 
                if(self.thrustData[counter][0] >= time):
                    # found the upper bound, do an interpolation,
                    thrust = self.thrustData[counter-1][1] + (self.thrustData[counter][1] - self.thrustData[counter-1][1])/(self.thrustData[counter][0] - self.thrustData[counter - 1][0]) * (time - self.thrustData[counter][0])
                    # do an impulse midpoint approximation 
                    impulse += (thrust + self.thrustData[counter-1][1])/2 * (time - self.thrustData[counter][0])
                    found = True
                else:
                    # do a midpoint impulse approximation 
                    midThrust = (self.thrustData[counter][1] + self.thrustData[counter-1][1])/2  
                    impulse += midThrust*(self.thrustData[counter][0] - self.thrustData[counter-1][0])
                counter += 1
            # calculate the motor weight by the proportion of impulse to totalImpulse 
            weight = self.motorDryWeight + self.motorPropWeight*(1-impulse/self.totalImpulse) 
            return [thrust,weight]

    # calculate some needed statistics including average thrust, total impulse, and burn duration 
    def computeStatistics(self):
        #compute some data for ease of access, including: average thrust, total impulse 
        #average thrust and total impulse use midpoint reimann sum 
        self.totalImpulse = 0
        for i in range(1,len(self.thrustData)):
            #calculate the midpoint 
            midThrust = (self.thrustData[i][1] + self.thrustData[i-1][1])/2  
            self.totalImpulse += midThrust*(self.thrustData[i][0] - self.thrustData[i-1][0])
        self.averageThrust = self.totalImpulse/ (self.thrustData[-1][0])
        self.burnTime = self.thrustData[-1][0] # not exactly the best way of doing this (motors sometimes trail off) 

    def parseFile(self): 
        data = open(self.file, 'r')
        self.thrustData = [] 
        for i,line in enumerate(data):
            # the first line should be a comment on the motor 
            if i == 0:
                # parse out the name of the motor, go until a character other than ';' or ' ' is found 
                counter = 0 
                found = False
                while(found == False and counter < len(line)):
                    if(line[counter] != ';' and line[counter] != ' '):
                        self.motorName = line[counter:].rstrip()
                        found = True
                    else:
                        counter += 1 
            elif i == 1: 
                # should be a set of data points for the motor. 
                info = line.split()
                self.motorDesignation = info[0]
                self.motorDiam = float(info[1])
                self.motorLength = float(info[2])
                # idk what the 4th info block is...
                self.motorPropWeight = float(info[4]) 
                self.motorTotalWeight = float(info[5])
                self.motorDryWeight = self.motorTotalWeight - self.motorPropWeight 
                self.motorManufacturer = info[6]
            # print(str((i+1)) + ": " + line,'')
            else: 
                # this is actual burn data  
                # separated into seconds thrust(N) 
                burnData = line.split()
                #print(burnData)
                #print(burnData[0])

                # store in [s,t] pairs 
                self.thrustData.append([float(burnData[0]), float(burnData[1])])



if __name__ == "__main__":
    # load up a sample data file 
    data = MotorDataReader("./Cesaroni_J760.eng")
    # print out some data from it 
    print(data.totalImpulse)
    print(data.averageThrust)
    print(data.getThrustWeight(0.1))