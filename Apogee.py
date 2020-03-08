
#const 
g = 9.81 


def determineApogee(s,v,k_m, time_step):
    position = [s]
    velocity = [v]
    acceleration = [-g - 1/2*k_m*v*v]
    time = [0]

    while(velocity[-1] > 0): 
        a_new = -g - 1/2*k_m*velocity[-1]*velocity[-1] 
        v_new = velocity[-1] + a_new * time_step
        s_new = position[-1] + v_new * time_step 
        position.append(s_new)
        velocity.append(v_new)
        acceleration.append(a_new)
        time.append(time[-1] + time_step) 
    print("Final Altitude: " + str(position[-1]))
    print("Time: " + str(time[-1]))



def main():
    print("Hello!")
    determineApogee(0,100,0,0.1)




if __name__ == "__main__":
    main() 