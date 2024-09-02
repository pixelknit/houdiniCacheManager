# Houdini Cache Manager
Houdini cache utilities for managing versions  

TOOL USAGE: This tool is a GUI that displays all the cache nodes in the Houdini scene,  
From left to right, the first column displays all the cache nodes, the next column displays  
the node types, the next column has a drop down menu, it displays the current cache version  
being used by each node and the final column has a drop down menu where you can see the unused caches.  
You can roll back versions, or change to any available cache, when you select a new cache, the node will use  
that selected cache and all the other caches will become unused, there is a button at the bottom to delete all  
unused caches, it will only delete caches with versions lower than the current one being used.  
![09](https://github.com/user-attachments/assets/ff9c91d5-a345-4f85-a4db-a0e0e7db8a0a)  

The tool is a Houdini python panel, it's using PySide2, QTWidgets, QtCore, but it relies on the main Houdini Python Panel API.
All the code for the panel is in the file cache_manager_panel.py. In order to use the tool you need to create a new python panel.  

Step 1) Set your Houdini project so it points to the right folder structure.  

![01_01](https://github.com/user-attachments/assets/7d21bab4-f3f3-46d8-ae1b-858f2c5ca1a9)  

Step 2) Go to Windows -> Python Panel Editor, in the Interfaces tab, click the New Interface button.  
Give your panel a name and label if you want, I'm calling mine Cache Utils, you can save it to the default  
location or to any other location. (Save to..).  

Step 3) Once your interface is saved, in the Python Panel Editor, change to the Pane Tab Menu tab, in here you'll see a list
of all the available interfaces on the left side, select your interface and click the right arrow to add it to your scene.  

![03](https://github.com/user-attachments/assets/df06d80d-6cf8-4a6c-afb7-a375ef028cf5)  

Step 4) Now that the interface lives in your scene you can access it in any pane, click the "+" icon -> New Pane Tab Type -> Misc -> Python Panel  
![05](https://github.com/user-attachments/assets/2282c300-51f2-494e-8f18-a3227c5050c5)  

Step 5) This will display the default python panel, in the drop down menu you'll have access to all the interfaces in your scene, so select yours.  

![06](https://github.com/user-attachments/assets/62c49dce-7e76-492d-9032-0b17ca0f1e14)  

Step 6) This will display your python panel, if you are creating it from scratch following this, the panel will be empty, maybe with the default "Hello World".  
So time to edit the panel and add the code, click the gear icon and select -> Edit Interface, this will open the Python Panel Editor again, copy/paste the code  
from the file "cache_manager_panel.py" into the script section, make sure you are editing your panel.  


![07](https://github.com/user-attachments/assets/85441974-1dc2-4100-8010-50fcaf63625f)  
![08](https://github.com/user-attachments/assets/4fd2b99b-9ba4-4635-8b8e-c1e18d31ecd8)  

After you paste the code click apply or accept and you'll have the full functional tool.

# TODO
-Automate this process with a shell or batch script.  
-Avoid the copy paste of the code and modularize it in the script sections.  
-Create classes for the functions in the main script.
