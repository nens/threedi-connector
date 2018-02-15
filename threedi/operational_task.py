"""
Dit script doet twee dingen:
    starten van een taak
    verwijderen oude saved state

Issue: result_uuid
"""
from datetime import datetime
import time
import httplib, urllib
import requests
import json
import getpass

password = getpass.getpass('Password:')

# Read previous_session_response file
previous_session_response = json.load(open('test.json'))
#print(previous_session_response['save_state_id'])

# time calculations
utcnow = datetime.utcnow()
secondsnow = time.mktime(utcnow.timetuple()) + utcnow.microsecond / 1E6

# create a "now" in two hours back in time to make sure data is available during testing with NRR data
false_now = secondsnow - (10.0 * 60.0) # ten minutes
secondshistory = secondsnow - (1 * 60.0 * 60.0) # 1 hours ago
secondsforecast = secondsnow + (3 * 60.0 * 60.0) # 3 hours ago

now = time.strftime('%Y-%m-%dT%H:%M', time.localtime(false_now))
history = time.strftime('%Y-%m-%dT%H:%M', time.localtime(secondshistory))
forecast = time.strftime('%Y-%m-%dT%H:%M', time.localtime(secondsforecast))

# start new calculation API POST
result = requests.post('https://staging.3di.lizard.net/api/v1/calculation/start/', 
	json={"organisation_uuid": "61f5a464c35044c19bc7d4b42d7f58cb",
    "model_slug": "v2_bergermeer-v2_bergermeer_bres_maalstop-55-784c561ecebf9433cd7beb8b6a22a14f2841cda4",
    "start": "%s" %(history),
    "end": "%s" %(forecast),
    "result_uuid": "%s" %(previous_session_response['result_id']), 
    "scenario_name": "nrr en harmonie",
    "rain_events": [
        {"type": "radar", "multiplier": 1, "active_from": "%s" %(history), "active_till": "%s" %(now), "start": "%s" %(history), "layer": "d6c2347d-7bd1-4d9d-a1f6-b342c865516f"},# NRR
        {"type": "radar", "multiplier": 1, "active_from": "%s" %(now), "active_till": "%s" %(forecast), "start": "%s" %(now), "layer": "a9c20cc2-1249-4458-a8b9-4cc76d3e5a51"}# Harmonie
    ],
    "use_saved_state": "%s" %(previous_session_response['save_state_id']),
	"save_states": [{"type": "timed", "t": "%s" %(now), "description": "%s" %(now)}],
	"store_results": {"process_basic_results": 'true'}}, 
	auth=('ber.albers', "%s" %(password)))

json_result = json.loads(result.text)

with open('test.json', 'w') as outfile:
    json.dump(json_result, outfile)

time.sleep(300)

threedimodelsavedstates_url = 'https://staging.3di.lizard.net/api/v1/threedimodelsavedstates/'
removal_url = threedimodelsavedstates_url + previous_session_response['save_state_id'] + '/'
save_state_removal = requests.delete(removal_url, auth=('ber.albers', "%s" %(password)))

print 'done'
