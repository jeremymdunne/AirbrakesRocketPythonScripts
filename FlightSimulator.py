from MotorDataReader import MotorDataReader
import matplotlib.pyplot as plt
import json 
import numpy
# const 
g = 9.81 


class Rocket:


    def __init__(self, motorData, dryMass, Base_Cd_data, standard_time_step):
        # initialize data 
        self.motor = motorData
        self.dryMass = dryMass
        self.Base_Cd_data = Base_Cd_data
        self.time_step = standard_time_step
        self.position = [0]
        self.velocity = [0]
        self.acceleration = [0]
        self.time = [0] 
    

    def calculate_boost_phase(self): 
        # boost phase 
        while(self.time[-1] <= self.motor.burnTime):
            self.time.append(self.time[-1] + self.time_step)
            [thrust,motorWeight] = self.motor.getThrustWeight(self.time[-1])  
            anew =  thrust/(self.dryMass + motorWeight) - g - self.calc_k(self.velocity[-1])*self.velocity[-1] * self.velocity[-1] / (self.dryMass + motorWeight)
            vnew = self.velocity[-1] + anew*self.time_step
            pnew = self.position[-1] + vnew*self.time_step + 1/2 * anew*self.time_step*self.time_step
            self.acceleration.append(anew) 
            self.velocity.append(vnew) 
            self.position.append(pnew)   
        #print(self.position[-1])


    def calc_k(self, v):
        # Cd values in mach number, Cd value pairs 
        # find the values we are in between 
        Cd = 0 
        if self.Base_Cd_data[0][0] >= v/343.0:
            Cd = self.Base_Cd_data[0][1]
        else:
            for i in range(1,len(self.Base_Cd_data)): 
                if(self.Base_Cd_data[i][0] > v / 343.0): 
                    # upper bound found, take the slope between the two 
                    Cd = self.Base_Cd_data[i-1][1] + (self.Base_Cd_data[i][1] - self.Base_Cd_data[i-1][1]) / (self.Base_Cd_data[i][0] - self.Base_Cd_data[i-1][0]) * (v / 343 - self.Base_Cd_data[i-1][0]) 
                    break
        #print(Cd)
        k_m = 1/2 * 1.225 * Cd * 0.01103224
        #print(k_m)
        return k_m 


    def calculate_next_position(self):
        # calculate for one time step out 
        self.time.append(self.time[-1] + self.time_step)
        anew = - g - self.calc_k(self.velocity[-1])*self.velocity[-1] * self.velocity[-1] / (self.dryMass + self.motor.motorDryWeight)
        vnew = self.velocity[-1] + anew*self.time_step
        pnew = self.position[-1] + vnew*self.time_step + 1/2 * anew*self.time_step*self.time_step
        self.acceleration.append(anew) 
        self.velocity.append(vnew) 
        self.position.append(pnew) 

    def calculate_coast_phase(self):
        while(self.velocity[-1] > 0):
            self.calculate_next_position() 

    def caluclate_remaining_flight(self):
        # start with the start variables currently, finish the flight, return the results, then reset to before 
        start_time = self.time.copy()
        start_position = self.position.copy()
        start_velocity = self.velocity.copy()
        start_acceleration = self.acceleration.copy()
        # assume we are in coast right now 
        self.calculate_coast_phase() 
        stored_time = self.time.copy()  
        stored_position = self.position.copy()
        stored_velocity = self.velocity.copy()
        stored_acceleration = self.acceleration.copy()
        # revert back to previous data 
        self.time = start_time 
        self.position = start_position 
        self.velocity = start_velocity 
        self.acceleration = start_acceleration 
        return [stored_time, stored_position, stored_velocity, stored_acceleration]


    def calculate_flight(self):
        # calculate the boost phase 
        self.calculate_boost_phase()
        # calculate the coast phase 
        self.calculate_coast_phase() 


    def create_sensor_data(self, exact, percent_standard_deviation, n_low, n_high, offset):
        noise = numpy.random.normal(0,percent_standard_deviation)
        data = numpy.random.uniform(n_low, n_high)*exact + noise/100*exact + offset
        return data


def main(): 

    # use a json file to access data 
    with open("./AirbrakeRocket.json",'r') as f: 
        data = json.load(f) 

    motorData = MotorDataReader(data["motor"])
    AirbrakeRocket = Rocket(motorData,data["dryMass"],data["baseCdValues"],.001)


    AirbrakeRocket.calculate_boost_phase()
    [time,position,velocity,acceleration] = AirbrakeRocket.caluclate_remaining_flight() 
    accel_sensor = acceleration.copy()
    for i in range(0,len(accel_sensor)):
        accel_sensor[i] = AirbrakeRocket.create_sensor_data(accel_sensor[i],2,0.995,1.005,1.5)
    time2 = time.copy()
    for t in time2:
        t = t + 1
    plt.plot(time, acceleration, label = "Exact Accel")
    plt.plot(time2, accel_sensor, label="Accel Sensor")
    plt.legend()
    plt.show()
    #print(position[-1])
    #AirbrakeRocket.dryMass = 12
    #AirbrakeRocket.calculate_coast_phase()
    #print(AirbrakeRocket.position[-1])

    
if __name__ == "__main__":
    main() 
