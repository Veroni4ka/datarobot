#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#

"""
To run the program type:
  $ python prediction.py 
"""

__author__ = ('veronika.kolesnikova@yahoo.com (Veronika Kolesnikova)')

import os
import pprint
import sys
import time

from apiclient import discovery
from apiclient import sample_tools
from oauth2client import client


# Time to wait (in seconds) between successive checks of training status.
SLEEP_TIME = 10



def print_header(line):
  '''Format and print header block sized to length of line'''
  header_str = '='
  header_line = header_str * len(line)
  print '\n' + header_line
  print line
  print header_line


def main(argv):
  
  service, flags = sample_tools.init(
      argv, 'prediction', 'v1.6', __doc__, __file__, 
      scope=('https://www.googleapis.com/auth/prediction', 'https://www.googleapis.com/auth/devstorage.full_control'))
  pid="spam"
  object_name="dr_hometask/english.csv"
  project="crested-surfer-91819"
  try:
    # Get access to the Prediction API.
    papi = service.trainedmodels()

    # List models.
    print_header('Fetching list of models')
    result = papi.list(project=project).execute()
    print 'List results:'
    pprint.pprint(result)

 # Start training request on a data set.
    print_header('Submitting model training request')
    body = {'id':pid, 'storageDataLocation':object_name}
    start = papi.insert(project=project, body=body).execute()
    print 'Training results:'
    pprint.pprint(start)

    # Wait for the training to complete.
    print_header('Waiting for training to complete')
    while True:
      status = papi.get(project=project, id=pid).execute()
      state = status['trainingStatus']
      print 'Training state: ' + state
      if state == 'DONE':
        break
      elif state == 'RUNNING':
        time.sleep(SLEEP_TIME)
        continue
      else:
        raise Exception('Training Error: ' + state)

      # Job has completed.
      print 'Training completed:'
      pprint.pprint(status)
      break

   #Analyze
    result = papi.analyze(id=pid, project=project).execute()
    print 'Analyze results:'
    pprint.pprint(result)

    # Make a prediction using the newly trained model.
    print_header('Making a prediction')
    body = {'input': {'csvInstance': ["Hey buy some stuff"]}}
    result = papi.predict(body=body, id=pid, project=project).execute()
    print 'Prediction results...'
    pprint.pprint(result)

    # Delete model.
    #print_header('Deleting model')
    #result = papi.delete(id=flag.id, project=flag.project).execute()
    #print 'Model deleted.'

  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")


if __name__ == '__main__':
  main(sys.argv)
