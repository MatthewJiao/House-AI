INPUT - from hospital; create text files for now

Pre-processing to get data to a specific format


Implement some rules based on certain values (subject to change)
    - age 16+
    - 
Return right away


Run through model
X amount of data ‘rows’
Output is prediction for the next ‘y’ hours with a confidence rating for each of them


Post-processing takes this output and checks it versus a ground truth of sepsis
    Gives percent of sepsis within next ‘a’, ‘b’, ‘c’, time period
    Might need weights on certain points and confidences

OUTPUT for now -  confidence levels

OUTPUT in future - Based on threshold, send to critical care team


For real time:
need to monitor many patients simulatenously; many streams of data coming in at intervals; need multiprocessing to handle this
- if rule or prediction happens - take off the worker