"""
Project: Project 4: CPU Scheduler
Author: Isaac Hill
Class: CS3060-X01
Last Updated: 3/15/2023
"""
import sys

#First Come, First Served
def fcfs(arrivalTimes, burstTimes):
    #Setup
    numOfProcesses = len(arrivalTimes)

    startTimes = []
    finishTimes = []
    responseTimes = []
    waitTimes = []
    turnAroundTimes = []

    clock = 0
    currentProcess = 0
    currentProcessFinish = 0
    readyQueue = []

    #Start first process
    clock = arrivalTimes[0]
    startTimes.append(arrivalTimes[0])
    currentProcessFinish = clock + burstTimes[0]

    #For each process
    for currentProcessLoopNum in range(numOfProcesses):
        #For each process after the current one
        for i in range(currentProcess + 1, numOfProcesses):
            #If the process arrives before the current process finishes and is arriving after current clock time and is not in the ready queue
            if(arrivalTimes[i] <= currentProcessFinish and arrivalTimes[i] >= clock and i not in readyQueue):
                #Update clock to the arrival time and add it to the ready queue
                clock = arrivalTimes[i]
                readyQueue.append(i)

        #Finish current process
        clock = currentProcessFinish
        finishTimes.append(currentProcessFinish)

        #If there is a process that is in ready queue
        if(readyQueue):
            currentProcess = readyQueue.pop(0)
            currentProcessFinish = clock + burstTimes[currentProcess]
            startTimes.append(clock)
        #Else if the current process is not the last process, wait for the next process
        elif(currentProcessLoopNum != numOfProcesses - 1):
            currentProcess = currentProcessLoopNum + 1
            clock = arrivalTimes[currentProcess]
            currentProcessFinish = clock + burstTimes[currentProcess]
            startTimes.append(clock)

        #Calculate response time, turn around time, and wait time for currentProcessLoopNum
        responseTimes.append(startTimes[currentProcessLoopNum] - arrivalTimes[currentProcessLoopNum])
        waitTimes.append(responseTimes[currentProcessLoopNum]) #in FCFS the wait time is the same as response time
        turnAroundTimes.append(finishTimes[currentProcessLoopNum] - arrivalTimes[currentProcessLoopNum])

    #Calculate Averages
    averageResponseTime = round(sum(responseTimes) / len(responseTimes), 2)
    averageWaitTime = round(sum(waitTimes) / len(waitTimes), 2)
    averageTurnAroundTime = round(sum(turnAroundTimes) / len(turnAroundTimes), 2)

    return averageResponseTime, averageTurnAroundTime, averageWaitTime


#Shortest Job First
def sjf(arrivalTimes, burstTimes):
    #Setup
    numOfProcesses = len(arrivalTimes)

    startTimes = []
    finishTimes = []
    responseTimes = []
    waitTimes = []
    turnAroundTimes = []

    clock = 0
    currentProcess = 0
    currentProcessFinish = 0
    readyQueue = []

    #Start first process
    clock = arrivalTimes[0]
    startTimes.append(arrivalTimes[0])
    currentProcessFinish = clock + burstTimes[0]

    #For each process
    for currentProcessLoopNum in range(numOfProcesses):
        #For each process after the first one
        for i in range(currentProcess + 1, numOfProcesses):
            #If the process arrives before the current process finishes and is arriving after current clock time and is not in the ready queue
            if(arrivalTimes[i] <= currentProcessFinish and arrivalTimes[i] >= clock and (i, burstTimes[i]) not in readyQueue):
                clock = arrivalTimes[i]
                #Store next processes in readyQueue in a tuple with the burst time
                readyQueue.append((i, burstTimes[i]))
                #Sort by burst time as to have shortest job first
                readyQueue.sort(key = lambda a: a[1])

        #Finish current process
        clock = currentProcessFinish
        finishTimes.append(currentProcessFinish)

        #Calculate response time, turn around time, and wait time for currentProcessLoopNum
        responseTimes.append(startTimes[currentProcessLoopNum] - arrivalTimes[currentProcess])
        waitTimes.append(responseTimes[currentProcessLoopNum]) #in SJF the wait time is the same as response time
        turnAroundTimes.append(finishTimes[currentProcessLoopNum] - arrivalTimes[currentProcess])

        #If there is a process that is in ready queue
        if(readyQueue):
            nextProcess = readyQueue.pop(0)
            currentProcess = nextProcess[0]
            currentProcessFinish = clock + nextProcess[1]
            startTimes.append(clock)
        #Else if the current process is not the last process, wait for the next process
        elif(currentProcess != numOfProcesses - 1):
            currentProcess = currentProcess + 1
            clock = arrivalTimes[currentProcess]
            currentProcessFinish = clock + burstTimes[currentProcess]
            startTimes.append(clock)

    #Calculated averages
    averageResponseTime = round(sum(responseTimes) / len(responseTimes), 2)
    averageWaitTime = round(sum(waitTimes) / len(waitTimes), 2)
    averageTurnAroundTime = round(sum(turnAroundTimes) / len(turnAroundTimes), 2)

    return averageResponseTime, averageTurnAroundTime, averageWaitTime


#Shortest Remaining Time First
def srtf(arrivalTimes, burstTimes):
    numOfProcesses = len(arrivalTimes)

    #Use None as to check for it later
    startTimes = [None] * numOfProcesses
    finishTimes = [None] * numOfProcesses
    stopTimes = [None] * numOfProcesses

    #Use 0s to += later
    responseTimes = [0] * numOfProcesses
    waitTimes = [0] * numOfProcesses
    turnAroundTimes = [0] * numOfProcesses

    #Initial Setup
    clock = 0
    currentProcess = 0
    currentProcessFinish = 0
    readyQueue = []
    inProgressProcesses = []

    #Start the first process
    clock = arrivalTimes[0]
    startTimes[0] = arrivalTimes[0]
    currentProcessFinish = clock + burstTimes[0]

    #While there is an unfinished process
    while None in finishTimes:
        #For each process after the current one
        for i in range(currentProcess + 1, numOfProcesses):
            #If the process arrives before the current process finishes and is arriving after current clock time and is not in the ready queue
            if(arrivalTimes[i] <= currentProcessFinish and arrivalTimes[i] >= clock and (i, burstTimes[i]) not in readyQueue):
                clock = arrivalTimes[i]
                #Store next processes in readyQueue in a tuple with the burst time
                readyQueue.append((i, burstTimes[i]))
                readyQueue.sort(key = lambda a: a[1])
                #If there is a shorter remaining time on the smallest process in readyqueue than the current process...
                if((readyQueue[0])[1] < currentProcessFinish - clock):
                    nextProcess = readyQueue.pop(0)
                    #Mark the stop time of the current running process
                    stopTimes[currentProcess] = clock
                    #Add the current process back in the readyQueue and add it also to inProgressProcesses with the current time remaining
                    readyQueue.append((currentProcess, currentProcessFinish - clock))
                    inProgressProcesses.append((currentProcess, currentProcessFinish - clock))
                    readyQueue.sort(key = lambda a: a[1])
                    currentProcess = nextProcess[0]
                    currentProcessFinish = clock + nextProcess[1]
                    startTimes[currentProcess] = clock

        #Finish current process
        clock = currentProcessFinish
        finishTimes[currentProcess] = (currentProcessFinish)

        #Calculate response time, turn around time, and wait time for currentProcessLoopNum
        responseTimes[currentProcess] += startTimes[currentProcess] - arrivalTimes[currentProcess]
        waitTimes[currentProcess] += startTimes[currentProcess] - arrivalTimes[currentProcess]
        turnAroundTimes[currentProcess] += finishTimes[currentProcess] - arrivalTimes[currentProcess]

        #If something is in readyQueue
        if(readyQueue):
            nextProcess = readyQueue.pop(0)
            if(nextProcess in inProgressProcesses):
                #Add how long the process had to wait to start back up again to process's waitTime
                waitTimes[nextProcess[0]] += clock - stopTimes[nextProcess[0]]
                inProgressProcesses.pop(inProgressProcesses.index(nextProcess))
                currentProcess = nextProcess[0]
                currentProcessFinish = clock + nextProcess[1]
            else:
                currentProcess = nextProcess[0]
                currentProcessFinish = clock + nextProcess[1]
                startTimes[currentProcess] = clock
        #Else if the current process is not the last process and there is a process waiting to be calculated
        elif(currentProcess != numOfProcesses - 1 and None in startTimes):
            currentProcess = startTimes.index(None)
            clock = arrivalTimes[currentProcess]
            currentProcessFinish = clock + burstTimes[currentProcess]
            startTimes[currentProcess] = clock

    #Calculate Averages
    averageResponseTime = round(sum(responseTimes) / len(responseTimes), 2)
    averageWaitTime = round(sum(waitTimes) / len(waitTimes), 2)
    averageTurnAroundTime = round(sum(turnAroundTimes) / len(turnAroundTimes), 2)

    return averageResponseTime, averageTurnAroundTime, averageWaitTime

#Round Robin
'''
NOT IMPLEMENTED CORRECTLY, doesn't loop and only does first 2 processes and returns None
I unfortunately didn't have time to finish :/
'''
def rr(arrivalTimes, burstTimes, timeQuantum):
    numOfProcesses = len(arrivalTimes)
    tq = timeQuantum

    #Use None as to check for it later
    startTimes = [None] * numOfProcesses
    finishTimes = [None] * numOfProcesses
    stopTimes = [None] * numOfProcesses

    #Use 0s to += later
    responseTimes = [0] * numOfProcesses
    waitTimes = [0] * numOfProcesses
    turnAroundTimes = [0] * numOfProcesses

    #Initial Setup
    clock = 0
    currentProcess = 0
    currentProcessFinish = 0
    quantumEnds = tq
    readyQueue = []
    inProgressProcesses = []

    #Start the first process
    clock = arrivalTimes[0]
    startTimes[0] = arrivalTimes[0]
    currentProcessFinish = clock + burstTimes[0]

    #For each process after the current one
    for i in range(currentProcess + 1, numOfProcesses):
        #If the process arrives before or at the time quantum
        if(arrivalTimes[i] <= quantumEnds and (i, burstTimes[i]) not in readyQueue):
            clock = arrivalTimes[i]
            #Store next processes in readyQueue in a tuple with the burst time
            readyQueue.append((i, burstTimes[i]))
            if(currentProcessFinish > quantumEnds):
                nextProcess = readyQueue.pop(0)
                stopTimes[currentProcess] = clock
                readyQueue.append((currentProcess, currentProcessFinish - clock))
                inProgressProcesses.append((currentProcess, currentProcessFinish - clock))
                currentProcess = nextProcess[0]
                currentProcessFinish = clock + nextProcess[1]
                startTimes[currentProcess] = clock
                break

    if(currentProcessFinish > quantumEnds):
        clock = quantumEnds
        quantumEnds += tq

    '''
    if(readyQueue):
        nextProcess = readyQueue.pop(0)
        if(nextProcess in inProgressProcesses):
            #Add how long the process had to wait to start back up again to process's waitTime
            waitTimes[nextProcess[0]] += clock - stopTimes[nextProcess[0]]
            inProgressProcesses.pop(inProgressProcesses.index(nextProcess))
            currentProcess = nextProcess[0]
            currentProcessFinish = clock + nextProcess[1]
        else:
            currentProcess = nextProcess[0]
            currentProcessFinish = clock + nextProcess[1]
            startTimes[currentProcess] = clock
    #Else if the current process is not the last process and there is a process waiting to be calculated
    elif(currentProcess != numOfProcesses - 1 and None in startTimes):
        currentProcess = startTimes.index(None)
        clock = arrivalTimes[currentProcess]
        currentProcessFinish = clock + burstTimes[currentProcess]
        startTimes[currentProcess] = clock
    '''

    print("-------------Current Clock Info-------------")
    print("Clock:", clock)
    print("Current Running Process:", currentProcess)
    print("Finishes:", currentProcessFinish)
    print("Quantum Ends:", quantumEnds)
    print("Ready Queue:", readyQueue)
    print("In Progress:", inProgressProcesses)
    print()
    print("StartTimes:", startTimes)
    print("FinishTimes:", finishTimes)
    print("StopTimes:", stopTimes)
    print()
    print("RTs:", responseTimes)
    print("WTs:", waitTimes)
    print("TATs:", turnAroundTimes)
    print()

    return None

def main():
    #Setup arrival and burst arrays and default timeQuantum
    arrivalTimes = []
    burstTimes = []
    timeQuantum = 100

    #Check if there is a time quantum for round robin given to replace the default
    if (len(sys.argv) != 1):
        timeQuantum = int(sys.argv[1])

    #Grab all arrival times and burst times and put them in their respective arrays
    for line in sys.stdin:
        splitLine = line.split()
        arrivalTimes.append(int(splitLine[0]))
        burstTimes.append(int(splitLine[1]))

    #First Come, First Served
    fcfsResults = fcfs(arrivalTimes, burstTimes)
    print("First Come, First Served")
    print("Avg. Resp.:%.2f, Avg. T.A.:%.2f, Avg. Wait:%.2f\n" % (fcfsResults[0], fcfsResults[1], fcfsResults[2]))

    #Shortest Job First
    sjfResults = sjf(arrivalTimes, burstTimes)
    print("Shrotest Job First")
    print("Avg. Resp.:%.2f, Avg. T.A.:%.2f, Avg. Wait:%.2f\n" % (sjfResults[0], sjfResults[1], sjfResults[2]))

    #Shortest Remaining Time First
    srtfResults = srtf(arrivalTimes, burstTimes)
    print("Shrotest Job First")
    print("Avg. Resp.:%.2f, Avg. T.A.:%.2f, Avg. Wait:%.2f" % (srtfResults[0], srtfResults[1], srtfResults[2]))

    #Round Robin
    #NOT IMPLEMENTED CORRECTLY, I didn't have time to finish :/
    '''
    rrResults = rr(arrivalTimes, burstTimes, timeQuantum)
    print("Shrotest Job First")
    print("Avg. Resp.:%.2f, Avg. T.A.:%.2f, Avg. Wait:%.2f\n" % (rrResults[0], rrResults[1], rrResults[2]))
    '''

if __name__ == "__main__":
    main()
