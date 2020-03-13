import numpy
import matplotlib.pyplot as plt 




def main(): 
    data = numpy.random.normal(0,1,1000)
    plt.hist(data,bins=10)
    plt.show()

main()