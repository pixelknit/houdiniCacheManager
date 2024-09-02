In the attachment you will find a Houdini project structure. `start_v001.hip` contains a scene that is creating some caches 
(each saved into `$HIP/caches/{cache_name}/{version}/{file_name}`). 
There are some old versions of these caches that are not being used by the scene anymore.

Write a tool to find caches that are not used in the scene and allows the user to delete them. 
Only allow the user to delete versions that are older than the version that is being used in the scene.

Bonus: Write functionality that allows the user to manage the cache versions that are loaded in their scene.