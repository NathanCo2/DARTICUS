"""!
\mainpage D.A.R.T.I.C.U.S.
This project was developed for the ME405 term project that required the development of a autonomous launcher. 
The goals of this project is to develop a thermal heating seeking dueling nerf gun turrent named D.A.R.T.I.C.U.S.
that can target and launch a projectile without user intervention. Our team was able to successfully design a
multitasking system that seemlessly integrated controls to operate the designed mechanical system.

D.A.R.T.I.C.U.S stands for: Dueling Autonomous infraRed Tracking IronClad Unrivaled Sentry. This name was
selected to intimidate our competition and convey the advanced capabilities of our autonomous launcher. By choosing
an acronym that evokes strength, precision, and cutting-edge technology, we aimed to assert out dominance in
the lab and showcase the exceptional capabilities of our project. The image below displays D.A.R.T.I.C.U.S in all
his glory. 
 
\image html Darticus.png width=500

\section Hardware
    
The blaster selected for this project was a Nerf Rival Knockout XX - 100 Blaster. After researching, it was
concluded this blaster met our system requirments with its high intensity and compact size. This spring-loaded
blaster is manually loaded and utilizing a slide-action mechanism that has a single-fire. To pull the trigger it
takes a 10lbf requiring us to carefully select a servo-motor that is capable of firing our system. A MG996R digital
servo motor was selected as it operates within the torque range required to pull the trigger, abot 12 kg-cm for 6V. 

This project was developed with utilizing two DC motors that contolled the x-axis of motion. One DC motor
is used for the 180 degree pivot that flips the blaster at the being of the duel using a pulley belt drive system.
This motor is the same that was used in our previous labs. The other DC motor utilized was a Metal Gearmotor 25D
MP 12V. This DC motor enabled a more accurate precision that was used to aim the blaster. It is important to note
that both motors were ran with an Encoder to ensure optimal movements from our system.

To enable the tracking  a thermal camera, a mlx90640 camera, was used that allowed our system to read the heat
signatures from the opposing team. The camera task will be futher elaborated on in the following sections.

    Bill of Materials:

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

Other materials not listed were 3D print or found around lab. This includes bolts, zip-ties, spare wood, and various
electrical components.


\section System Tasks
There are a total of four task that run our design system. These task entail Pivot, Aim, Fire, and Track. A task
diagram was developed and designed to layout the set of task for our multitasking system. The 
of importnace of each task. For our system is This is the overall task diagram that was implement to run our system. 
This section will break down the task that are preformed in the main section of our program. Each section will 

\subsection Pivot

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