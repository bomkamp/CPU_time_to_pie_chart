#@AUTHOR: Greg Bomkamp
#@DATE: 10/12/2016
#@INPUTS: 1) Name of an input file in the same directory as program. This file will be a .CSV in the format: <USER>,<PID>,<PROCESS CPU TIME>,<TOTAL CPU TIME>
#         2) Name of the output graph image in the form: <NAME>.png
#@OUTPUT: A PNG image of a pie graph that shows the total cpu usage split into users which each user divided into their processes.
#@DESC: Program Program is composed of two functions, processData() that will manipilate the CSV file into an array containing all process information and createGraph() to output a graph using the array from processData()

import matplotlib.pyplot as plot
import matplotlib.patches as mpatches
from collections import OrderedDict

#Function to process CSV file into a workable array
def processData(data):
    processes=[]
    dataFile = open(data,'r')
    processLine = dataFile.read()
    while(processLine):
        singleProcessData = processLine.strip().replace('\n',',').split(',')
        processes += singleProcessData
        processLine = dataFile.read()
        return processes

#Function to output a graph based on the array from processData()
def createGraph(processes,output):
    cumulativeTotal=0
    total=int(processes[3])
    colors=['red','blue','green','yellow','purple','orange','gray','orange','indigo'] #supports a max of 9 users because i could only think of 9 colors
    colorIndex=0
    processIndex=0
    #create arrays to generate graph
    currentColor=""
    currentUser=""
    userIDs=[]
    processIDs=[]
    colorIDs=[]
    timeslices=[]
    while(processIndex<len(processes)):
    
        if currentUser!=processes[processIndex]:
            #new user => update color
            currentUser=processes[processIndex]
            currentColor=colors[colorIndex]
            colorIndex+=1

        #fill each array to supply to matplotlib of data for graphs
        userIDs.append(currentUser)
        colorIDs.append(currentColor)
        processIDs.append(processes[processIndex+1])
        timeslices.append(int(processes[processIndex+2]))
        cumulativeTotal+=int(processes[processIndex+2])
        #increment by 4 to next process
        processIndex+=4
        
    #UNCOMMENT IF ROOT SHOULD CONTAIN ANY LEFTOVER CPU TIME NOT USED BY THE OTHER PROCESSES
    ####Add final element of left over CPU time that is root processes####
    #userIDs.append('root')
    #processIDs.append('0')
    #colorIDs.append('white')
    #timeslices.append(total-cumulativeTotal)
    
    #Arrays are populated to call to matplotlib to create pie graph with the new data.
    for i in range(0,len(processIDs)): processIDs[i]='PID: '+processIDs[i]
    patches = plot.pie(timeslices,colors=colorIDs,labels=processIDs,shadow=True,autopct='%1.1f%%')
    userIDs=list(OrderedDict.fromkeys(userIDs))
    colorIDs=list(OrderedDict.fromkeys(colorIDs))
    
    #Add a legend by removing duplicates from user array and creating a patch for each user with a color
    handles=[]
    for i in range(0,len(userIDs)):
        patch=mpatches.Patch(color=colorIDs[i],label=userIDs[i])
        handles.append(patch)
    plot.legend(handles=handles,loc="lower left",shadow=True,borderaxespad=-2,ncol=len(userIDs))

    #title the graph
    plot.title('Fair Share Usage Graph')
    #Save graph to png file named the given name
    #plot.tight_layout()
    plot.figsize=(20,20)
    plot.savefig('./'+output)

#start main execution
data=input('Enter the name of the datafile: ')
output=input('Enter the name of the output graph: ')
processes=processData(data)
createGraph(processes,output)

exit
