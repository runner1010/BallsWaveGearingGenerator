# BallsWaveGearingGenerator
Wave Transmission Calculator with Intermediate Rolling Elements

Translation of - https://boosty.to/trashrobotics/posts/ab3f6701-b668-4861-923f-f213840cb547

To build a wave reducer with PTC and simplify my work, I wrote a script for calculating and building its profile.
It can be found at: https://codeberg.org/TrashRobotics/BallsWaveGearingGenerator
Or the translated file in this repository: calc_vptc.py

It is a Python script in which you need to enter data about your gearbox (gear ratio 𝐢, diameter of the balls used 𝐝𝐬𝐡 and outer radius of the hard wheel depressions 𝐑𝐨𝐮𝐭). 
Also, before running the script, you need to install additional libraries for Python (if they are not already installed):
$ pip3 install ezdxf matplotlib numpy

When launched, the script will calculate all the parameters of the reducer, generate a full profile of the reducer and output it to a dxf file with the name you specify in the 𝐎𝐔𝐓_𝐅𝐈𝐋𝐄 variable.

Then the file can be imported into any CAD and the gearbox can be modeled.

Some subtleties regarding the choice of the outer radius of the hard drive dimples 𝐑𝐨𝐮𝐭.

The smaller it is, the more compact the gearbox will be. But there is a limit to which it can be reduced. It is determined by the following formula:
$R_{BH} \leq \frac{1.03 * d_{\omega(p)}}{sin(\pi / Z_{x})}$

But don't worry, if you overdo it, the calculator will tell you.
