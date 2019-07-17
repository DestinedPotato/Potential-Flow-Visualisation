import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from tkinter import *

#######################################
###########Maths part of code##########
#######################################

def jouk(z, lamd, alpha):
    joukowsky = z + (np.exp(-1j*2*alpha)*lamd**2)/z #This transforms all of the points on the circle using the Joukowsky transformation
    return joukowsky

def circlemake(C, r):
    t = np.linspace(0,2*np.pi, 200) #This collects all of the points on a linear space between two points
    circle = C+r*np.exp(1j*t) #This converts points collected into a circle
    return circle

def deg2rad(deg):
    rad = (deg*np.pi)/180 #A simple degrees to radian conversion
    return rad

def flowlines(alpha, r, beta, v_inf, ratio):
    #ratio = r/lamd
    alpha = deg2rad(alpha) #Both alpha and Beta are inputted in degress where as they need to be in radians
    beta = deg2rad(beta)
    if ratio<=1:
        raise ValueError("r/Lambda must be >1")
    lamd = r/ratio

    centre_c = np.exp(1J*alpha)*(lamd-r*np.exp(-1j*beta))

    circle = circlemake(centre_c,r)    #Creation of the original circle
    airfoil=jouk(circle, lamd, alpha)  #Creation of the original airfoil
    bigx = np.arange(-3,3.1, 0.1)
    bigy = np.arange(-3,3.1, 0.1)
    x,y = np.meshgrid(bigx,bigy)    #The two x and y componets are put in to a matrix
    z = x+1j*y #The combination of the x and y components into the z component
    z=ma.masked_where(np.absolute(z-centre_c)<=r, z)
    w=jouk(z, lamd, alpha)
    beta = beta + alpha
    z2 = z-centre_c
  
    gamma = -4*np.pi*v_inf*r*np.sin(beta)       #This sets up a variable that will be used in the final calculation    
    u2=np.zeros(z2.shape, dtype=np.complex)     #Another variable being set up for the final calculation    
    with np.errstate(divide='ignore'):
        for m in range(z2.shape[0]):
            for n in range(z2.shape[1]):

                u2[m,n]=gamma*np.log((z2[m,n])/r)/(2*np.pi)    #This is where the Array is calculated the be used in the final calculation
    c_flow = v_inf*z2 + (v_inf*r**2)/z2 - 1j*u2     #This is where the flow is actually calculated
##### Maths test Section ######
    velocity = np.array(np.diff(c_flow)/np.diff(z))
    grad = np.array(np.gradient(velocity))
    divergence = np.sum(grad, axis=0)
    print("Average Divergence",np.average(divergence))
    print("Average Velocity", np.average(velocity))
#### Maths test Section ######
    return (w, c_flow, airfoil)

def get_contours(mplcont):
    conts=mplcont.allsegs   #Converts the flow into points that can be plotted
    xline=[]                #The Array for all x coordinates
    yline=[]                #the Array for all y coordinates

    for  cont in conts:     #This for loop converts all the values into coordinates that can be plotted
        if len(cont)!=0:
            for arr in cont: 
                
                xline+=arr[:,0].tolist()
                yline+=arr[:,1].tolist()
                xline.append(None) 
                yline.append(None)
    

    return xline, yline
#############################################
###########Tkinter Section of Code###########
#############################################

def flowlinesmake(beta=5, v_inf=1, ratio = 1.2):
    plt.cla()
    alpha = 0                                      
    alpha = (w2.get())                                  #This gets all the information from the UI and makes it usable for the rest of the program
    r = 0
    r = (w1.get())
    r += 1

    (w, c_flow, airfoil) = flowlines(alpha, r, beta, v_inf, ratio)  #This calls the flowlines function with the inputs from the user
    cp = plt.contour(w.real, w.imag, c_flow.imag)                        #This turns all of the results into something that MatPlotLib can plot
    xline, yline = get_contours(cp)
    plt.plot(airfoil.real, airfoil.imag)        #This is where all of the results are plotted into a singular MatPlotLib graph
    plt.plot([xline],[yline])
    plt.show()


master = Tk()
master.title("Potential Flow Visualisation") #This changes the title of the window
w1 = Scale(master, from_=0.00, to=1.00, resolution=0.01, label='c')
w1.set(0.00)
w1.grid(row=0, column=0)
w2 = Scale(master, from_=0, to=90, label='Angle of Attack')
w2.set(0)
w2.grid(row=0,column=1)


updatebutton = Button(master, text='Update Flow', command=flowlinesmake).grid(row=1,column=2)
exitbutton = Button(master, text='Exit', command=quit).grid(row=2,column=2)

mainloop()
