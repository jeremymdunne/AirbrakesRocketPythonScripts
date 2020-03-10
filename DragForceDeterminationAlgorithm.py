g = 9.81
 
def calc_apo(s,v, k_m, time_step):
    position = [s]
    velocity = [v]
    acceleration = [-g - 1/2*k_m*v*v]
    time = [0] 
    # seed a s, v, a value 
    while(velocity[-1] > .000001):
        anew =  - g - 1/2*k_m*velocity[-1] * velocity[-1]
        #print((anew + g))
        vnew = velocity[-1] + acceleration[-1]*time_step
        if(vnew < 0):
            vnew = 0
        pnew = position[-1] + velocity[-1]*time_step + 1/2 * acceleration[-1]*time_step*time_step
        acceleration.append(anew) 
        velocity.append(vnew) 
        position.append(pnew)   
        time.append(time[-1] + time_step) 
        #print(velocity[-1])

    #print("Final position: " + str(position[-1]))
    #print("Time: " + str(time[-1]))
    return position[-1]

def calculate_require_drag_force(wanted_apo, k_m, v, time_step):
    # calculate the required k_m to reach the wanted apo 
    
    # assume the initial step in k_m is .0001 
    k_m_guess = [k_m]
    k_m_guess.append(k_m + .0000001)
    apos = [calc_apo(0,v,k_m,time_step)]
    apos.append(calc_apo(0,v,k_m_guess[-1],time_step))
    #print(apos[-1])
    converg = 1 
    print((apos[-1] - wanted_apo)/((apos[-2] + apos[-1])/(k_m_guess[-2] - k_m_guess[-1])))
    while(converg > .0005):
        k_m_guess.append(k_m_guess[-1] - (apos[-1] - wanted_apo)/((apos[-2] - apos[-1])/(k_m_guess[-2] - k_m_guess[-1]))) 
        print(k_m_guess[-1])
        apos.append(calc_apo(0,v,k_m_guess[-1],time_step))
        print(apos[-1])
        converg = abs((k_m_guess[-1] - k_m_guess[-2])/k_m_guess[-1])
    return k_m_guess[-1]






def main(): 
   apo = calc_apo(0,174.65,0.00290561621,0.0001)
   print(apo)
   print(calculate_require_drag_force(550, 0.00290561621, 174.65, 0.01))


if __name__ == "__main__":
    main() 