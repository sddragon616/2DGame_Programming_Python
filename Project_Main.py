import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "SDL2\\x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "SDL2\\x64"


import Project_SceneFrameWork
import Scene000_Logo

Project_SceneFrameWork.run(Scene000_Logo)
