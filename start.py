from subprocess import Popen, PIPE
import os

logpath = 'C:/Users/SIDDHARTHABHATTACHAR/Documents/Copy/MachineLearning/sampleProjects/logbotFramework/'


processes = [[['python', 'botController.py'], 'botController_out.log', 'botController_err.log'],
[['python', './apis/intentController.py'], 'intentController_out.log', 'intentController_err.log'],
[['python', './apis/test/cities.py'], 'cities_out.log', 'cities_err.log']]


plist = [Popen(n[0], stdout=PIPE, stderr=PIPE) for n in processes]
try:
    for proc in plist:
        proc.wait()
except KeyboardInterrupt:
    for proc in plist:
        try:
            proc.terminate()
        except OSError as e:
            print(e)
        proc.wait()

