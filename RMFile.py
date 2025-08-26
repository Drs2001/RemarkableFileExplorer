from RM_API import RM_API

class RMFile():
    """
    A class used to store and represent a file from the file system on a Remarkable Tablet device.
    A file can either be a CollectionType which is a folder containing other files, or a DocumentType
    which is a pdf or remarkable document with no children.

    ...

    Attributes
    ----------
    bookmarked : bool
        Tells wheather the file has been bookmarked on the tablet
    ID : str
        The ID of the file
    modified_client : DateTime
        The last time the file was modified on the tablet
    type : str
        The type of file it is either 'CollectionType' or 'DocumentType'
    vissibleName : str
        The name of the file on the tablet
    parent : RMFile
        The parent file/folder of the current file
    children : list(RMFile)
        The list of children this file/folder has
    """
    def __init__(self, file, parent=None):
        """
        Parameters
        ----------
        file : Dictionary
            The data of the file used to create out object
        parent : The parent object of this file 
        """
        api = RM_API()
        self.__bookmarked = file['Bookmarked']
        self.__ID = file['ID']
        self.__modified_client = file['ModifiedClient']
        self.__type = file['Type']
        self.__vissibleName = file['VissibleName']
        self.__parent = parent
        self.__children = []

        if self.__type == 'CollectionType':
            files = api.get_directory(self.__ID)
            for file in files:
                tempFile = RMFile(file, self)
                self.__children.append(tempFile)
    
    def get_name(self):
        """Gets the name of the file

        Returns
        -------
        str
            The files name
        """
        return self.__vissibleName
    
    def get_id(self):
        """Gets the id of the file

        Returns
        -------
        str
            The files id
        """
        return self.__ID
    
    def get_type(self):
        """Gets the type of the file(either 'CollectionType' or 'DocumentType')

        Returns
        -------
        str
            The files type
        """
        return self.__type
    
    def get_children(self):
        """Gets the children of the file if it is a 'CollectionType'

        Returns
        -------
        list
            The files children
        """
        return self.__children
