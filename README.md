# PFG
## Basic description.
This is the main repository for my final degree proyect. It basically consists in a end-point detection system of ransomware based on it's behavour. It will have seeral stages:
1. Gathering all the information and bibliography.
2. Buiding a program for the following platforms: Android, Windows and Linux. The idea of this program is collecting all the relevant data concerning the machine behavour, so we can disguise if it's an infected one (with any kind of ransomware) or not. The nature of this data is (by now) of three types: network activity, APIs and System calls (depending on which OS are we refering) and hardware resources use.
3. Buiding another program that will be alocated in the "network manager" host. It will collect all the data from the machines in the network and send it to the cloud (see steep 4). It will also receive the alerts from the cloud in case of detecting a suspicious behavour in one of the machines.
4. Create a data lake in the Azure Cloud and create a detection system usion ML and AI tools. After creating and training the model, it will scan all the data sent by the program in step 3 and send the proper alert if necessary.

## Current stage of the proyect.
I'm still gathering infromation and developing some scripts for the step 2.


---



# Actual notes about development.
In order to go with step 2 development, I've divided the kind of data we should collect in three types: network data, HW resources data and Log and event data. 

# Bibliographic aproaches.

## Useful info regarding each OS.

### Andoid

There is some interesting references in the survey [(Cen, 2023)](https://drive.google.com/file/d/1gDN4WYrqDrvKwQ9MQQxUuXCnOZvOMlZf/view?usp=drive_link) regarding early detection solutions for Android in refs. 63-74.

## Useful info regarding the data I should look for.

### Network data.
I still have to decide wether to use a different tool per each OS or to use psutils for all of them. Look for what kind of info uses other realted works.

According to ref [(Schoenbachler, 2023)](https://drive.google.com/file/d/1UnIbWdUNv8WK9_bSsCPjqGDaKZr2R7Pf/view?usp=drive_link/), it's a good idea to look for the number of different hosts connectec, UDP connections made and DNS connections. I assume that the relevant fact is the number. 



### HW activity and performance.
In [(Alam, 2018)](https://drive.google.com/file/d/1Sv0PCjQSWHR4QB3pADWbKkMS6PUE3gQm/view?usp=drive_link), they develop a RAPPER (Ransomware Prevention via Performance Counter), and they use HPCs for this performance evaluation. Maybe is a good idea to use them along with psutils library.


### Registry events, API calls and filesystem activity (OS related activity)
In [(Ganfure, 2020)](https://drive.google.com/file/d/1VRWqS83AVqN8JwuVcMT-_DXu-_utwsCY/view?usp=drive_link) they develop a detector using the filesystem activity: 
```
we propose a simple but effective
concept of user-file interaction modeling with deep generative
autoencoder architecture. Unlike other works aiming to look at
ransomware signature or dynamic behavior, this work aimed to
capture a legitimate user’s behavior by logging the recurrence
of user-file interaction such as create, delete, changed, and
rename operations every t seconds.
```


---


# To do list

[x] Develop the program that collect the data for Windows.

[] Develop the program that collect the data for Android.

[] Develop the program that collect the data for Linux.

[] Make a list of important items to look for in the network case.

[] Make a list of important items to look for in the HW case.

[] Make a list of important items to look for in the  case.
