from MotorDataReader import MotorDataReader
# const 
g = 9.81 


def calc_k(v):
    # Cd values in mach number, Cd value pairs 
    Cd_values = [   [.01,0.49], [0.06,0.41], [0.11,0.42], [0.16,0.42], [0.21,0.42], [0.26,0.43], [0.31,0.44], [0.36,0.44], [0.41,0.45], [0.46,0.47], [0.51,0.48], [0.56,0.5], [0.61,0.51], [0.66,0.54], [0.71,0.56], [0.76,0.6],[0.81,0.64], [0.86,0.7], [0.91,0.77], [0.96,0.76], [1.01,0.76] ]    
    # find the values we are in between 
    Cd = 0 
    if Cd_values[0][0] >= v/343.0:
        Cd = Cd_values[0][1]
    else:
        for i in range(1,len(Cd_values)): 
            if(Cd_values[i][0] > v / 343.0): 
                # upper bound found, take the slope between the two 
                Cd = Cd_values[i-1][1] + (Cd_values[i][1] - Cd_values[i-1][1]) / (Cd_values[i][0] - Cd_values[i-1][0]) * (v / 343 - Cd_values[i-1][0]) 
                break

    #print(Cd)
    k_m = 1/2 * 1.225 * Cd * 0.01103224
    #print(k_m)
    return k_m 

def calculate_path(time_step,motorData,rocket_mass):
    position = [0]
    velocity = [0]
    acceleration = [0]
    time = [0] 
    # boost phase 
    while(time[-1] <= motorData.burnTime):
        time.append(time[-1] + time_step)
        [thrust,motorWeight] = motorData.getThrustWeight(time[-1])  
        anew =  thrust/(rocket_mass + motorWeight) - g - calc_k(velocity[-1])*velocity[-1] * velocity[-1] / (rocket_mass + motorWeight)
        vnew = velocity[-1] + anew*time_step
        pnew = position[-1] + vnew*time_step + 1/2 * anew*time_step*time_step
        acceleration.append(anew) 
        velocity.append(vnew) 
        position.append(pnew)   
    print(position[-1])
    # coast phase 
    while(velocity[-1] >= 0):
        time.append(time[-1] + time_step)
        anew = - g - calc_k(velocity[-1])*velocity[-1] * velocity[-1] / (rocket_mass + motorData.motorDryWeight)
        vnew = velocity[-1] + anew*time_step
        pnew = position[-1] + vnew*time_step + 1/2 * anew*time_step*time_step
        acceleration.append(anew) 
        velocity.append(vnew) 
        position.append(pnew)   

    #print("Final position: " + str(position[-1]))
    #print("Time: " + str(time[-1]))
    return[position,velocity,acceleration,time]


def main(): 
    motorData = MotorDataReader("./Cesaroni_J760.eng")
    #print(motorData.totalImpulse)
    [s,v,a,t] = calculate_path(.001,motorData,6.1235)
    print(s[-1])
    #print(v[-1])
    
if __name__ == "__main__":
    main() 
