import requests
import sys

class RM_API():
    def __init__(self):
        self.RM_URL = 'http://10.11.99.1'

    def printTreeStructure(self, parentID=None, depth=0, withID=False):
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
