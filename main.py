import requests
import sys

RM_URL = 'http://10.11.99.1'

def printTreeStructure(parentID=None, depth=0):
    directoryMetadataUrl = RM_URL + '/documents/'

    if parentID is not None:
        directoryMetadataUrl = directoryMetadataUrl + parentID

    try:
        response = requests.get(directoryMetadataUrl)
    except Exception as e:
        print("Error: Unable to establish connection to tablet. Make sure the tablet is plugged in and USB sharing is enabled in the settings.")
        sys.exit()

    response.encoding = 'UTF-8'
    metaData = response.json()
    
    for data in metaData:
        # Print out the remarkable file structure as a tree
        if depth==0:
            print(data['VissibleName'])
        else:
            print(depth*"   " + "|__" + depth*" " + data['VissibleName'])

        if data['Type'] == 'CollectionType':
            printTreeStructure(data['ID'], depth+1)


if __name__ == "__main__":
    printTreeStructure()
