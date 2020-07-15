import requests, json, csv

username = 'youraccountname' #account username
poesessid = 'fundingsekiroshadowdiethrice' #chrome://settings/cookies/detail?site=pathofexile.com
tabindex = ['17','18'] #count starts at 0, put tabs containing only horticrafting benches


def combineResponseLists(dict1, dict2):
    itemlist = dict1["items"] + dict2["items"]#
    return itemlist

def grabTabDataToJSON(tabIndex):
    url = 'https://www.pathofexile.com/character-window/get-stash-items?league=Harvest&tabs=0&tabIndex=' + str(tabIndex) + '&accountName=' + username
    payload = {'POESESSID' : poesessid}
    response = requests.post(url, cookies=payload)
    return response.json()

def removeGGGtextformatting(uglystring):
    uglystring = uglystring[0:-5] #take out seed ilvl
    cleanstring = uglystring.replace("<white>", "")
    cleanstring = cleanstring.replace("{", "")
    cleanstring = cleanstring.replace("}", "")    
    return cleanstring

def getDuplicatesWithCount(listOfElems):
    ''' Get frequency count of duplicate elements in the given list '''
    dictOfElems = dict()
    # Iterate over each element in list
    for elem in listOfElems:
        # If element exists in dict then increment its value else add it in dict
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1    
 
    # Filter key-value pairs in dictionary. Keep pairs whose value is greater than or equal 1 i.e. combine only duplicate elements from list.
    # dictOfElems = { key:value for key, value in dictOfElems.items() if value >= 1}
    # Returns a dict of duplicate elements and thier frequency count
    return dictOfElems

def makelistpretty(fixthislist):
    augs = []
    lucky_augs = []
    removes = []
    remove_add = []
    removenon_add = []
    reforges = []
    divines = []
    resistbending = []
    implictshit = []
    exchange = []
    sacrifice = []
    bethechangeyouwanttosee = []
    miscshit = []
    #empty = ['']

    for craft in fixthislist:
        #print(craft)
        if (craft.find('non-') != -1)  & (craft.find('remove') != -1 ):
            removenon_add.append(craft)
        elif (craft.find('remove')!= -1) & (craft.find('add') != -1 ):
            remove_add.append(craft)
        elif (craft.find('reforge') != -1):
            reforges.append(craft)
        elif (craft.find('augment') != -1) & (craft.find('lucky') != -1):
            lucky_augs.append(craft)
        elif (craft.find('augment') != -1):
            augs.append(craft)
        elif (craft.find('remove') != -1):
            removes.append(craft)
        elif (craft.find('randomise') != -1) or (craft.find('reroll') != -1):
            divines.append(craft)
        elif (craft.find('change a modifier that grants') != -1):
            resistbending.append(craft)
        elif (craft.find('set a new implicit') != -1) or (craft.find('synthesised implicits') != -1):
            implictshit.append(craft)
        elif (craft.find('sacrifice') != -1):
            sacrifice.append(craft)
        elif (craft.find('exchange') != -1):
            exchange.append(craft)
        elif (craft.find('change') != -1) and  (craft.find('change a modifier') == -1):
            bethechangeyouwanttosee.append(craft)                 
        else:
            miscshit.append(craft)
            #print("fucked up")
    prettylistfinal = ['\nLUCKY AUGS======, Craft Quantity']+lucky_augs+ ["\nAUGS======="]+ augs + ['\nREMOVE=====']+  removes + ["\nREMOVE/ADD====="]+  remove_add + ["\nREMOVE-NON/ADD========"]+  removenon_add + ["\nREFORGES======="]+  reforges + ["\nDIVINING====="]+ divines+ ["\nRESIST CHANGING====="]+ resistbending +["\nADDING IMPLICITS ======"]+ implictshit+ ["\nSACRIFICE===="]+ sacrifice+ ["\nEXCHANGE====="]+ exchange+ ["\nCHANGE====="]+ bethechangeyouwanttosee + ["\nMISC======"]+ miscshit
    #prettylistfinal = remove_add
    
    return prettylistfinal


#going through tabindex and grabbing the item info
for i in range(len(tabindex)):
    if i == 0: #for first tab
        firsttab = grabTabDataToJSON(tabindex[i])
        response1 = firsttab

    if i > 0: #for tabs after first
        response2 = grabTabDataToJSON(tabindex[i])        
        combinedItemslist = combineResponseLists(response1, response2)
        combinedItemsdict = {'items': combinedItemslist}
        response1 = combinedItemsdict


#Start processing the 'items' dict
#
benchlist = [] #nested list of crafts in each bench
notcountedlist = [] #unsorted list of crafts all expanded out
js = combinedItemsdict.get('items')
for i in js:
    benchlist.append(i.get('craftedMods')) #each bench is a list with crafts ['x','y','z']

#seperating crafts from benches to individual lines
for i in benchlist:
    for j in i:
        uglystring = j #take out seed ilvl
        beautifulstring = removeGGGtextformatting(uglystring)
        notcountedlist.append(beautifulstring) #going to seperate list for sorting

countedlist = [] #almost home

# Get a dictionary containing duplicate elements in list and their frequency count
dictOfcrafts = getDuplicatesWithCount(notcountedlist)

for key, value in dictOfcrafts.items():
    countedlist.append('"' + key + '"' +","+ str(value)) #csv format, using "" to keep commas inside craft descrptions for csv export

countedlist = [item.lower() for item in countedlist] #lower case everything to be searchable
prettylistfinalfinal = makelistpretty(countedlist) #pass countedlist into the sorter to combine counted craft types

#begin writing to csv
outputFile = open('horti_crafts.csv', 'w')

for craftline in prettylistfinalfinal:
    outputFile.write( craftline + '\n') #already in csv format, just seperate lines
    

outputFile.close()
