"""!
\mainpage D.A.R.T.I.C.U.S.
This project was developed for the ME405 term project that required the development of an autonomous launcher. 
The goal of this project is to develop a thermal heating seeking dueling Nerf gun turret named D.A.R.T.I.C.U.S.
that can target and launch a projectile without user intervention. Our team was able to successfully design a
multitasking system that seamlessly integrated controls to operate the designed mechanical system.

D.A.R.T.I.C.U.S stands for: Dueling Autonomous infraRed Tracking IronClad Unrivaled Sentry. This name was
selected to intimidate our competition and convey the advanced capabilities of our autonomous launcher. By choosing
an acronym that evokes strength, precision, and cutting-edge technology, we aimed to assert our dominance in
the lab and showcase the exceptional capabilities of our project. The image below displays D.A.R.T.I.C.U.S in all
his glory. 
 
\image html Darticus.png width=500

\section Hardware
    
The blaster selected for this project was a Nerf Rival Knockout XX - 100 Blaster. After researching, it was
concluded this blaster met our system requirements with its high intensity and compact size. This spring-loaded
blaster is manually loaded and utilizes a slide-action mechanism that has a single fire. To pull the trigger it
takes a 10lbf requiring us to carefully select a servo-motor that is capable of firing our system. An MG996R digital
servo motor was selected as it operates within the torque range required to pull the trigger, about 12 kg-cm for 6V.

This project was developed by utilizing two DC motors that controlled the x-axis of motion. One DC motor
is used for the 180-degree pivot that flips the blaster at the being of the duel using a pulley belt drive system.
This motor is the same one that was used in our previous labs. The other DC motor utilized was a Metal Gearmotor 25D
MP 12V. This DC motor enabled a more accurate precision that was used to aim the blaster. It is important to note
that both motors were run with an Encoder to ensure optimal movements from our system.

To enable the tracking a thermal camera, a mlx90640 camera, was used that allowed our system to read the heat
signatures from the opposing team. The camera task will be further elaborated on in the following sections.

\subsection iBOM

Bill Of Materials

    Part                                    Quantity            Description
    ---------------------------------------------------------------------------------------
    Blaster                                     1          Nerf Rival Knockout XX - 100 Blaster
    Stepper Motor                               1          For precise rotational movement
    Medium Density Fireboard Wood               1          For structural support
    6" Lazy Susan                               2          For smooth rotation
    Wood Screws                                 1          For assembly
    Machine Screw Zinc Screws                   1          For assembly
    Lab DC Motors                               1          For additional functionality
    Metal Gearmotor 25D                         1          Used to have more precise movements

Other materials not listed were 3D printed or found around the lab. This includes bolts, zip-ties, spare wood, and various
electrical components.

\subsection Modeling

The following images display the developed CAD drawings that were utilized to house the Metal Gearmotor 25D MP 12V.
The internal gears used to drive the aiming task of our system utilized a 3:1 ratio. The image below shows a view inside
the chamber and the gears used to drive the base of the Lazy Susan.

\image html Clearview.png width=500 
\image html InternalGears.png width=500

\section Software Organization
The following files are used in order to operate our system:


\section System Tasks
There are a total of four tasks that run our design system. These tasks entail Pivot, Aim, Fire, and Track. A task
diagram was developed and designed to layout the set of task for our multitasking system. The importance of each task
was determined along with the associated frequency. An image of the developed task diagram can be seen below that was
used to run our system.

\image html taskdiagram.png width=500 

Mirroring a similar behavior to the developed task diagram, the finite state machine (FSM) developed for the overall system
mimics the same pattern. An image of the FSM is shown below.

\image html systemfsm.png width=500 

It is important to note that for our multi-tasking system shares are used to facilitate communication and data sharing
among different task that are running concurrently. Each share in this system either set as a flag or set to a specfied
value. The four shares used in this program are GO1, GO2, bullseye, and kill. The GO1 and GO2 shares are used as a flag
to communicate that the following task is completed. The bullseye share is used to convey the angle of the tracked target
from the thermal camera to the aiming task. The kill share is used to terminate the task and stop the operation of the
system. By using shares, task are able to communciate effectively and allows D.A.R.T.I.C.U.S to achieving the desired
functionality. 

This following subsections will break down the task that are preformed in the main section of our program. Each section
will elaborate on the states used for each task. 

\subsection Pivot
The Pivot task is responsible for turning the 

\subsection Aim

\subsection Fire

\subsection Track



"""

# \subsubsection sub1 State 1
# to use same name later just need
# \subsubsection sub 1
# \image html imagename.png/.jpg width=500 "WILL NOT LOAD IMAGE UNTIL DOXY HAS A IMAGE DIRECTROY"
# \section {section-name} "DO NOT USE SPACES!'
# \subsection {subsection.name} {Title}
# \subsubsection {subsection-name} {Title}


