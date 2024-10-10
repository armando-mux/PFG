# PFG
## Basic description.
This is the main repository for my final degree proyect. It basically consists in a end-point detection system of ransomware based on it's behavour. It will have seeral stages:
1. Gathering all the information and bibliography.
2. Buiding a program for the following platforms: Android, Windows and Linux. The idea of this program is collecting all the relevant data concerning the machine behavour, so we can disguise if it's an infected one (with any kind of ransomware) or not. The nature of this data is (by now) of three types: network activity, APIs and System calls (depending on which OS are we refering) and hardware resources use.
3. Buiding another program that will be alocated in the "network manager" host. It will collect all the data from the machines in the network and send it to the cloud (see steep 4). It will also receive the alerts from the cloud in case of detecting a suspicious behavour in one of the machines.
4. Create a data lake in the Azure Cloud and create a detection system usion ML and AI tools. After creating and training the model, it will scan all the data sent by the program in step 3 and send the proper alert if necessary.

## Current stage of the proyect.
I'm still gathering infromation and developing some scripts for the step 2.
