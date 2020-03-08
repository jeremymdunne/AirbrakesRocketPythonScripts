import matplotlib.pyplot as plt
from math import cos, pi

# constants 
g = 9.81



def get_set_point_altitude(cur_apogee, time_to_apogee, target_apogee, time_step):
    
    set_point = -(cur_apogee - target_apogee)/(time_to_apogee)*time_step + cur_apogee
    if(set_point < target_apogee):
        set_point = target_apogee
    return set_point


def calc_k_m(v):
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
    k_m = 1/2 * 1.225 * .91 * 0.008129016 / 2.15456
    #print(k_m)
    return k_m 



def calculate_path(s,v, k_m, time_step):
    position = [s]
    velocity = [v]
    acceleration = [-g - calc_k_m(v)*v*v]
    time = [0] 
    # seed a s, v, a value 
    while(velocity[-1] > 0):
        anew =  - g - calc_k_m(velocity[-1])*velocity[-1] * velocity[-1]
        #print((anew + g))
        vnew = velocity[-1] + acceleration[-1]*time_step
        pnew = position[-1] + velocity[-1]*time_step + 1/2 * acceleration[-1]*time_step*time_step
        acceleration.append(anew) 
        velocity.append(vnew) 
        position.append(pnew)   
        time.append(time[-1] + time_step) 

    #print("Final position: " + str(position[-1]))
    #print("Time: " + str(time[-1]))
    return[position,velocity,acceleration,time]




def main(): 
    # set up some data to simulate 
    # start with some data from Ben's flight 
    apo = 12000
    a_target = 10000
    initial_time_to_apo = 10
    time_to_apo = initial_time_to_apo
    set_points = [apo]
    time_points = [0]

    while(time_to_apo > 0.001 and set_points[-1] > a_target):
        if(len(set_points) > 1):
            wanted_apo_change = (set_points[-1] - set_points[-2])
        else:
            wanted_apo_change = set_points[-1] - apo
        #print(cos(2*(initial_time_to_apo - time_to_apo)*pi))
        actual_apo_change = wanted_apo_change * (cos(5*(initial_time_to_apo - time_to_apo)*pi)*.5 + .6) 
        #print(actual_apo_change)
        #print(actual_apo_change)
        if(len(set_points) > 1):
            set_points.append(get_set_point_altitude(set_points[-2] + actual_apo_change, time_to_apo, a_target, .01)) 
        else: 
            set_points.append(get_set_point_altitude(apo + actual_apo_change, time_to_apo, a_target, .01)) 
        time_to_apo = time_to_apo - .01 
        #print(set_points[-1])
        time_points.append(initial_time_to_apo - time_to_apo) 
    plt.plot(time_points, set_points, label = "Setpoint")
    plt.title("Setpoint vs Time")
    plt.show()


    



if __name__ == "__main__":
    main()