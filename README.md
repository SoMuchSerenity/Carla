# Log of Carla implementation

## 31/5

Done: 

1. Successfully installed Carla in remote Linux server.  
2. Installed Pycharm

To-do:  

1. Fix TCP port problems 
2. Run manual_control.py
3. Write a script to allow agent to move always forward



## 02/06

Done:

1. Bought a new laptop

To-do:  

1. Learn RLlib
2. Read source code of Carla's RLlib integration 
3. try RLlib on gym's car racing
4. Run manual_control.py
5. Write a script to allow agent to move always forward

Deprecated:

1. Install Carla in remote Linux Server


## 22/06

Done:
1. A simple demo showing how to spawn a vehicle with different sensors installed and retrieving data.
2. Run mannual_control.py
3. Write a script to allow agent to move always forward

To-do:
1. Learning RLlib(learning)
2. Read source code of Carla's RLlib integration(reading)
3. Try RLlib on gym's car racing
4. Write a Carla custom enviroment for RLlib


## 23/06
Done: 
1. Write a Carla custom enviroment for RLlib(partly done)

To-do:
1. Learning RLlib(learning)
2. Read source code of Carla's RLlib integration(reading)
3. Try RLlib on gym's car racing
4. Investigate syncing
5. Know how to load data from RAM 
6. Figure out the best way to train, online/offline/traning data storage
7. Building value neural network and policy network
8. Design a proper reward function

Issues fixed:
https://github.com/opencv/opencv-python/issues/631	No hint provided in Pycharm for the newest version of OpenCV, 4.2.0.32 compatible

https://github.com/carla-simulator/carla/issues/4940	Carla crashes in low quality in towns except for 01. Known issue in Carla.

Issue remained: 

https://github.com/carla-simulator/carla/issues/5502	No rendering option still outputs data

##  15/07

Done:
1. Write a Carla custom enviroment for RLlib(fully done).
2. Building value neural network and policy network.
3. Design a proper reward function.

To-do:
1. Debug learn() and start to train the agent on laptop, later train in the server.
2. Replace resnet18 with efficientnet.
3. Implement Beta Distribution for action space.

Issue fixed:

https://github.com/carla-simulator/carla/issues/5502	Able to using command line to disable rendering. Code in the file does not work.

Issue remained:

https://github.com/DLR-RM/stable-baselines3/issues/961	Invalid index to scalar variable when indexing action space, which is supposed to be np.array and can be indexed.