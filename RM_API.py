import requests
import sys

class RM_API():
    """
    Class to interface with the Remarkable Tablets web based API

    ...

    Attributes
    ----------
    RM_URL : str
        The url that the Remarkable tablets web api address is at
    """
    def __init__(self):
        self.RM_URL = 'http://10.11.99.1'

    def printTreeStructure(self, parentID=None, depth=0, withID=False):
        """Prints the file structure of the connected Remarkable Tablet

        Parameters
        ----------
        parentID : str
            The ID of the parent directory to start printing from, default is the root
        depth : int
            Simple int to control spaces when printing
        withID : bool
            Controls wether to print with the documents ID or not
        """
        url = self.RM_URL + '/documents/'

        if parentID is not None:
            url = url + parentID

        try:
            response = requests.get(url)
        except Exception as e:
            print("Error: Unable to establish connection to tablet. Make sure the tablet is plugged in and USB sharing is enabled in the settings.")
            sys.exit()

        response.encoding = 'UTF-8'
        metaData = response.json()
        
        for data in metaData:
            # Print out the remarkable file structure as a tree
            if depth==0:
                print(data['VissibleName'] + (":" + data['ID'] if withID else ""))
            else:
                print(depth*"   " + "|--" + depth*" " + data['VissibleName'] + (":" + data['ID'] if withID else ""))

            if data['Type'] == 'CollectionType':
                self.printTreeStructure(data['ID'], depth+1, withID)

    def get_directory(self, id=None):
        """Gets all the files of the directory, defaults to root

        Parameters
        ----------
        id : str
            The ID of the directory to get files from

        Returns
        -------
        list
            a list of dictonarys representing the files on the Remarkable
        """
        url = self.RM_URL + '/documents/'
        if id is not None:
            url = url + id
        
        try:
            response = requests.get(url)
        except Exception as e:
            print("Error: Unable to establish connection to tablet. Make sure the tablet is plugged in and USB sharing is enabled in the settings.")
            sys.exit()

        response.encoding = 'UTF-8'
        metaData = response.json()
        return metaData
