# DARTICUS
 
Meet DARTICUS aka Dueling Autonomous infraRed Tracking IronClad Unrivaled Sentry! The purpose behind DARTICUS is to provide 
users who want to have a Nerf blaster duel with friends an autonomous method to compete in these duels. This allows users to 
spend all their energy dodging incoming bullets whilst DARTICUS does all the work in terms of aiming and firing at the opponent. 
From working on DARTICUS, members of the team have learned how to design, integrate, wire and program a mechatronics system. 
More specifically, the students have learned how to design motor and servo classes which allow them to drive multiple motor 
objects for the base pulley system and the top geared system. 

 <img width="452" alt="Darticus" src="https://github.com/NathanCo2/DARTICUS/assets/156122419/812084c6-8635-43fa-9f2c-7f92980e53db">

DARTICUS is broken down into three main subsystems: the base pulley system, the top geared system, and the servo trigger system. 
The base pulley system and the top geared system are designed to provide rotation about the z-axis to spin DARTICUS. The base 
pulley system is designed to pan the Nerf blaster the necessary 180 degrees to face the opponent. This subsystem is designed to 
provide a fast and repeatable method of spinning the blaster 180 degrees by choosing to operate the bottom DC motor at a higher 
speed while giving up accuracy. To compensate for the decreased accuracy, the 3D-printed coupler has a hard stop built into the 
design which interfaces with a stopper bolted to the base of DARTICUS. On the other hand, the top geared system is set to operate 
at a slower speed but at a higher accuracy using a gear ratio of 1:3. The Nerf Rival blaster is attached to the top mount plate 
using a mount that matches the rail profile at the top of the Nerf blaster. This mount angles the blaster at a 4-degree offset 
to account for the distance between DARTICUS and the opponent. The servo trigger system utilizes a standoff adapter on the servo 
horn to engage with the Nerf blaster trigger. The servo is securely attached to the Nerf blaster. To integrate the servo into the 
electronics of DARTICUS, a voltage regulator needed to be implemented. Due to the DARTICUS requiring a 12V power supply for the 
motors, the input voltage needed to be reduced to the specifications of the servo. By adding the voltage regulator and capacitors, 
the input voltage for the servo is now 5V. To locate the opponent, a thermal camera is used to measure the heat signature of the 
person. This camera is mounted on a stand that is placed at the middle of the distance between DARTICUS and the opponent. On the 
off chance, DARTICUS malfunctions you can pull the bundled-up red wires to cut power to the servo and the motors. 

<img width="245" alt="taskdiagram" src="https://github.com/NathanCo2/DARTICUS/assets/156122419/5eccd2cb-d0d3-4128-8b99-2d2b20ce43f6">

The software architecture for DARTICUS is broken down into four main tasks which uses multitasking through the function cotask. 
The task of the highest priority is the “Aim” task. The Aim task uses the target angle obtained from the camera reading to tell 
the motor what setpoint it needs to angle the Nerf blaster in the direction of the target. Once the task is completed, it sets 
the GO2 flag true (GO2 = 1) and puts it into a share to communicate with other tasks in the future. The next task in terms of 
next highest priority is the “Pivot” task. The Pivot task is responsible for driving the base pulley motor which has a predefined 
setpoint to achieve the desired 180-degree rotation at the beginning of the duel. This motor only utilizes proportional control 
to achieve the desired behavior in a short time. Once this task is completed, the GO1 flag will be set to True (GO1 = 1) which 
uses a share to communicate with future tasks. Both tasks utilize the motor class to use the attributes setup in the motor driver, 
encoder reader, and motor controller files developed in previous labs. The task that is 3rd in priority is the “Track” task. The 
Track task is where the code for the I2C is implemented to read values from the camera. The camera gets a thermal reading and 
extracts the column with the highest average heat signature. Then the tasks will calculate the angle that DARTICUS needs to rotate 
in order to aim at the target measured by the camera and place it into a share for the Aim task. Lastly, the “Fire” task has the 
lowest priority and has the purpose of triggering the servo to actuate the blaster trigger. The task looks to set whether the GO1 
and the GO2 flags are True before moving the servo which ensures that the blaster is oriented in the correct direction. Please refer 
to the Doxygen documentation to learn more about the software: 

[ADD LINK HERE].

To develop a functional system, our team developed the code for each individual task to check verify that the base code functions 
properly before integrating multitasking with cotask. Once the code for each task was developed, our team first tested the code 
for the Pivot task. The goal was to test multiple proportional control values to determine what proportional gain would be best 
suited for our system. Nathan’s advanced controls term project models the a PID controller for the motor used in the top geared 
system. This model helped provide insight into starting the proportional, integral and derivative gains values used to test the 
motor in the Aim task. Afterwards, our team integrated all the tasks together and ran multiple tests to fine tune the period of 
each tasks, the PID controller gains, the setpoint for the Pivot task and the angle offset conversion for the camera. At first, 
the test we ran would inconsistently hit the target. After the tuning, DARTICUS was able to hit the target at a more consistent rate. 

Our team has learned a lot from developing DARTICUS. We learned how to develop drivers to control both the pulley driven and gear 
driven motor. Using two different motors to rotate about the z-axis aided us in fine tuning our device for optimal performance. 
The pulley driven motor only utilized proportional control to allow it to have the fastest response time to rotate the 180 degrees. 
This allowed our team to get a faster response time while using a hardware stopper to achieve our desired accuracy. Then, the geared
motor used PID control and operates at a slower speed to achieve more accurate control. Through developing DARTICUS, our team members
learned to develop a controller for the servo as well as convert to get angle as the input. From implementation of cotask, we learned
to implement shares to transfer data from task to task as well as tune ther period and priority to optimize DARTICUS’s performance. 
We were also able to learn key lessons from translating DARTICUS from a CAD to real hardware. The gears we designed for the precise 
aiming of the blaster were a little smaller than we thought after we 3D printed them. As a result, there was play in the gears which
led to decreases accuracy in aiming the blaster. We suggest that better sized gears are printed for future iterations of DARTICUS. 
We also suggest that a hub with a setscrew is printed with the gear mounted to the motor as the D bore on the gear kept getting stripped. 
The last suggestion is to get a faster camera if you want to aim at moving targets. The current camera installed doesn’t allows the 
loop to run fast enough to capture the location, aim and shoot at the moving target in a timely manner.
