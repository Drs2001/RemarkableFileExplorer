from RM_API import RM_API
from RMFile import RMFile

class RMFileTree():
    """
    A class used to store and represent the file system on a Remarkable Tablet device.

    ...

    Attributes
    ----------
    baseDir : List(RMFile)
        The list of files in the base directory of the tablet
    currentDir : List(RMFile)
        The list of files in the current operating directory of the tablet
    """
    def __init__(self):
        """
        Parameters
        ----------
        """
        api = RM_API()
        self.__baseDir = []
        files = api.get_directory()
        for file in files:
            tempRMFile = RMFile(file)
            self.__baseDir.append(tempRMFile)
        
        self.__currentDir = self.__baseDir
    
    def get_current_dir(self):
        return self.__currentDir