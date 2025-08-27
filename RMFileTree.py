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
    previousDir : List(RMFile)
        The list of files in the previous directory the user was in
    """
    def __init__(self):
        api = RM_API()
        self.__baseDir = []
        files = api.get_directory()
        for file in files:
            tempRMFile = RMFile(file)
            self.__baseDir.append(tempRMFile)
        
        self.__currentDir = self.__baseDir
        self.__previousDir = []
    
    def get_current_dir(self):
        """Gets the current dir the user is in

        Returns
        -------
        list
            The files in the directory
        """
        return self.__currentDir
    
    def get_base_dir(self):
        """Gets the root dir

        Returns
        -------
        list
            The files in the root directory
        """
        return self.__baseDir
    
    def update_current_dir(self, dir):
        """Updates the current directory to the one passed in

        Parameters
        ----------
        dir : list(RMFiles)
            The directory to update to
        """
        self.__previousDir.append(self.__currentDir)
        self.__currentDir = dir
    
    def back_to_previous(self):
        """Updates the current directory to the previous one
        """
        if len(self.__previousDir) != 0:
            index = len(self.__previousDir) - 1
            self.__currentDir = self.__previousDir[index]
            self.__previousDir = self.__previousDir[:-1]
        else:
            self.__currentDir = self.__baseDir
