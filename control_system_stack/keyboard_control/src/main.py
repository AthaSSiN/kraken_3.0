import roslib;roslib.load_manifest('keyboard_control')

from Tkinter import *
import rospy
from std_msgs.msg import String
from kraken_msgs.msg import forceData6Thruster
from resources import topicHeader

root = Tk()

frame = Frame(root, width=100, height=100)

label_vars = range(6)

for i in range(len(label_vars)):
    label_vars[i] = StringVar()
    label_vars[i].set('empty')

def editGui(data):

    for i in range(len(data.data)):
        label_vars[i].set(data.data[i])

    if FIRST_ITERATION:

        present6.data[0] = previous6.data[0] = data.data[0]
        present6.data[1] = previous6.data[1] = data.data[1]
        present6.data[2] = previous6.data[2] = data.data[2]
        present6.data[3] = previous6.data[3] = data.data[3]
        present6.data[4] = previous6.data[4] = data.data[4]
        present6.data[5] = previous6.data[5] = data.data[5]


        FIRST_ITERATION = False

    previous6.data[0] = data.data[0]
    previous6.data[1] = data.data[1]
    previous6.data[2] = data.data[2]
    previous6.data[3] = data.data[3]
    previous6.data[4] = data.data[4]
    previous6.data[5] = data.data[5]

    # print data.data
    # print type(data)
    # print data.data[0]

rospy.init_node('keyboard_control_vehicle_node', anonymous=True)
rospy.Subscriber(topicHeader.CONTROL_PID_THRUSTER6, forceData6Thruster, editGui)
pub6 = rospy.Publisher(topicHeader.CONTROL_PID_THRUSTER6, thrusterData6Thruster, queue_size = 2)

present6 = thrusterData6Thruster()
previous6 = thrusterData6Thruster()
THRUSTER_VALUES_CHANGED = False
FIRST_ITERATION = True

r = rospy.Rate(10)

while not rospy.is_shutdown():

    # pub4.publish(thruster4Data)

    if THRUSTER_VALUES_CHANGED:

        pub6.publish(present6)
        THRUSTER_VALUES_CHANGED = False

    else:

        pub6.publish(previous6)
        
    r.sleep()

# Force Defination
# force[0] = forward thruster on left side, positive value takes vehicle forwards
# force[1] = forward thruster on right side, positive value takes vehicle forwards
# force[2] = sway thruster on front side, positive value takes vehicle rightwards
# force[3] = sway thruster on back side, positive value takes vehicle rightwards
# force[4] = depth thruster on back side, positive value takes vehicle downwards
# force[5] = depth thruster on front side, positive value takes vehicle downwards

# Keyboard Control

# w - forward
# a - left
# s - backward
# d - right
# t - top (towards the surface)
# g - ground (towards the pool bottom)

string_dict = {0 : "left", 1 : "right", 2 : "backward", 3 : "forward", 4 :
        "top", 5 : "bottom", 6 : "STOP"}

def create_callbacks(arg):

    def callback(ev=None):

        '''
        the argument consists the thruster number whose value has to be changed.

        global variable previous6 has the current values of thrusters. 

        We will have to put the new value into present6 and 
        then return from this function. This will publish the value in present6
        instead of previous6, thus changing the values given to the thrusters.
        '''

        global present6
        global previous6
        global THRUSTER_VALUES_CHANGED

        present6.data[0] = previous6.data[0]
        present6.data[1] = previous6.data[1]
        present6.data[2] = previous6.data[2]
        present6.data[3] = previous6.data[3]
        present6.data[4] = previous6.data[4]
        present6.data[5] = previous6.data[5]


        if arg == 0:

            present6.data[4] = previous6.data[4] - MIN_THRUST_INPUT
            present6.data[5] = previous6.data[5] + MIN_THRUST_INPUT

        if arg == 1:

            present6.data[4] = previous6.data[4] + MIN_THRUST_INPUT
            present6.data[5] = previous6.data[5] - MIN_THRUST_INPUT

        if arg == 2:

            present6.data[4] = previous6.data[4] - MIN_THRUST_INPUT
            present6.data[5] = previous6.data[5] - MIN_THRUST_INPUT

        if arg == 3:

            present6.data[4] = previous6.data[4] + MIN_THRUST_INPUT
            present6.data[5] = previous6.data[5] + MIN_THRUST_INPUT

        if arg == 4:

            present6.data[0] = previous6.data[0] - MIN_THRUST_INPUT
            present6.data[1] = previous6.data[1] - MIN_THRUST_INPUT

        if arg == 5:

            present6.data[0] = previous6.data[0] + MIN_THRUST_INPUT
            present6.data[1] = previous6.data[1] + MIN_THRUST_INPUT

        if arg == 6:

            present6.data[0] = 0.
            present6.data[1] = 0.
            present6.data[2] = 0.
            present6.data[3] = 0.
            present6.data[4] = 0.
            present6.data[5] = 0.

        THRUSTER_VALUES_CHANGED = True

    return callback
    
left = Button(frame, text="left(A)", command=create_callbacks(0))
left.grid(row=1,column=0)

back = Button(frame, text="backward (S)", command=create_callbacks(2))
back.grid(row=1,column=1)

right = Button(frame, text="right (D)", command=create_callbacks(1))
right.grid(row=1,column=2)

forward = Button(frame, text="forward (W)", command=create_callbacks(3))
forward.grid(row=0,column=1)

top = Button(frame, text="top (T)", command=create_callbacks(4))
top.grid(row=0,column=3)

bottom = Button(frame, text="bottom (G)", command=create_callbacks(5))
bottom.grid(row=1,column=3)

stop = Button(frame, text="STOP (Space)", bg='red', command=create_callbacks(6))
stop.grid(row=1,column=4)

l1 = Label(frame, text="Force Values")
l1.grid(row=0, column=5)

for i in range(6):
    temp = Label(frame, textvariable=label_vars[i])
    temp.grid(row=i+1, column=5)

root.bind("a", create_callbacks(0))
root.bind("d", create_callbacks(1))
root.bind("s", create_callbacks(2))
root.bind("w", create_callbacks(3))
root.bind("t", create_callbacks(4))
root.bind("g", create_callbacks(5))
root.bind("<space>", create_callbacks(6))

frame.pack()

root.mainloop()
