# Before running the script, install the libraries (if they are not already installed):
import ezdxf                        #
import matplotlib.pyplot as plt     #
import sys                          # $ pip3 install ezdxf matplotlib numpy
import numpy as np                  #

""" Script for calculating and constructing a profile of a wave gearbox with intermediate rolling elements (WRE)
Author: Artem TrashRobotics
Channel: https://www.youtube.com/@trashrobotics
Boosty: https://boosty.to/trashrobotics
Git: https://codeberg.org/TrashRobotics

In general, enter the basic data (gear ratio, ball diameter, rigid wheel profile radius) for the gearbox you need and the script will automatically calculate all the parameters and build: 
1) rigid wheel profile (BASE_WHEEL_SHAPE) 
2) separator (SEPARATOR) 
3) wave generator/eccentric (ECCENTRIC) 
4) balls (BALLS) 
5) gearbox outer diameter (OUT_DIAMETER) 

After which it will write everything to a file with DXF resolution, which can be opened in any CAD.
"""
OUT_FILE = "vptc6.dxf" # Name of the file to which the profile will be saved
RESOLUTION = 600 # Number of points for constructing the profile of the rigid wheel
i = 17 # The gear ratio you need
dsh = 6 # Diameter of the balls from the bearing
Rout = 38 # Outer radius of the troughs of the rigid wheel
D = 90 # Outer diameter of the gearbox (optional)
u = 1 # Number of waves created by the wave generator (DO NOT TOUCH, because it was not calculated for more than 1)

# Flags that determine which profiles will be built and transferred to the drawing. Those that are not needed can be disabled
BASE_WHEEL_SHAPE = True
SEPARATOR = True
ECCENTRIC = True
BALLS = False       # for demonstration only (DO NOT transfer to the drawing: you will get confused. The balls are not located at equal distances from each other)
OUT_DIAMETER = True
""" --------------------------------------------------------------------------------------- """
""" Everything below you no longer need, it will work itself. Or will say: why does it not work """
""" --------------------------------------------------------------------------------------- """

e = 0.2 * dsh
zg = (i+1)*u
zsh = i
Rin = Rout - 2*e
rsh = dsh/2
rd = Rin + e - dsh
hc = 2.2*e
Rsep_m = rd + rsh
Rsep_out = Rsep_m + hc/2
Rsep_in = Rsep_m - hc/2

print("........................")
print("Main parameters of the VPTK:")
print("- Gear ratio: ", i)
print("- Eccentricity: ", e)
print("- Eccentric radius: ", rd)
print("- Outer radius of the rigid wheel profile: ", Rout)
print("- Inner radius of the rigid wheel profile: ", Rin)
print("- Number of depressions of the rigid wheel profile: ", zg)
print("- Number of balls: ", zsh)
print("- Ball diameter: ", dsh)
print("- Separator pitch radius: ", Rsep_m)
print("- Separator thickness: ", hc)
print("........................")
print("........................")

if Rin <= ((1.03 * dsh)/np.sin(np.pi/zg)):
    print("This won't work -_-)")
    print("The inner radius of the hard wheel troughs Rin({0}mm) must be greater than: {1}mm. Increase Rout or decrease the "
"gear ratio (i)!".format(Rin, (1.03 * dsh)/np.sin(np.pi/zg)))
    sys.exit(1)

#print(rd/rsh, 0.65*zg+2.8)

theta = np.linspace(0, 2*np.pi, RESOLUTION)

S = np.sqrt((rsh + rd) ** 2 - np.power(e * np.sin(zg * theta), 2))
l = e * np.cos(zg * theta) + S
Xi = np.arctan2(e*zg*np.sin(zg*theta), S)

x = l*np.sin(theta) + rsh * np.sin(theta + Xi)
y = l*np.cos(theta) + rsh * np.cos(theta + Xi)

xy = np.stack((x, y), axis=1)


sh_angle = np.linspace(0, 1, zsh+1) * 2*np.pi
S_sh = np.sqrt((rsh + rd) ** 2 - np.power(e * np.sin(zg * sh_angle), 2))
l_Sh = e * np.cos(zg * sh_angle) + S_sh
x_sh = l_Sh*np.sin(sh_angle)
y_sh = l_Sh*np.cos(sh_angle)


doc = ezdxf.new("R2000")
msp = doc.modelspace()

if BASE_WHEEL_SHAPE:
    msp.add_point([0, 0])
    msp.add_lwpolyline(xy)
    # msp.add_circle((0, 0), radius=Rout)
    # msp.add_circle((0, 0), radius=Rin)

if SEPARATOR:
    msp.add_circle((0, 0), radius=Rsep_out)
    msp.add_circle((0, 0), radius=Rsep_in)

if ECCENTRIC:
    msp.add_point([0, e])
    msp.add_lwpolyline([[0, 0], [0, e]])
    msp.add_lwpolyline([[-6, 0], [6, 0]])
    msp.add_lwpolyline([[-3, e], [3, e]])
    msp.add_circle((0, e), radius=rd)

if BALLS:
    for i in range(zsh):
        msp.add_circle((x_sh[i], y_sh[i]), radius=rsh)

if OUT_DIAMETER:
    msp.add_circle((0, 0), radius=D/2)

doc.saveas(OUT_FILE)

print("Профиль построен и записа в файл:", OUT_FILE)

# Additional visualization of the result in matplotlib
if True:
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(x, y, linewidth=1.0)
    ax.plot([0, 0], (0, e), ".", linewidth=1.0)
    ax.plot([-6, 6], (0, 0), "--k", linewidth=1.0)
    ax.plot([-3, 3], (e, e), "--k", linewidth=1.0)
    D_circle = plt.Circle((0, 0), D / 2, color='b', fill=False, linewidth=1.0)
    rd_circle = plt.Circle((0, e), rd, color='b', fill=False, linewidth=1.0)
    Rsep_out_circle = plt.Circle((0, 0), Rsep_out, fill=False, linewidth=1.0)
    Rsep_in_circle = plt.Circle((0, 0), Rsep_in, fill=False, linewidth=1.0)
    ax.add_patch(D_circle)
    ax.add_patch(rd_circle)
    ax.add_patch(Rsep_out_circle)
    ax.add_patch(Rsep_in_circle)

    for i in range(zsh):
        sh_circle = plt.Circle((x_sh[i], y_sh[i]), rsh, color='r', fill=False, linewidth=1.0)
        ax.add_patch(sh_circle)

    # test = plt.Circle((0, 0), Rin, color='g', fill=False, linewidth=1.0)
    # ax.add_patch(test)
    # test2 = plt.Circle((0, 0), Rout, color='g', fill=False, linewidth=1.0)
    # ax.add_patch(test2)
    plt.show()

