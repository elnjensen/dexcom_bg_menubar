#!/usr/bin/env python3

# If the script fails to find Python, you may need to change the first
# line to give the explicit path to your Python executable, e.g.
#!/opt/homebrew/bin/python3
# or
#!/Users/username/anaconda3/bin/python

# <xbar.title>Dexcom BG</xbar.title>
# <xbar.version>1.0</xbar.version>
# <xbar.author>Eric Jensen</xbar.author>
# <xbar.author.github>elnjensen</xbar.author.github>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.desc>Displays blood glucose data from Dexcom Share</xbar.desc>
# <xbar.var>string(VAR_USERNAME=""): Your Dexcom username.</xbar.var>
# <xbar.var>string(VAR_PASSWORD=""): Your Dexcom password.</xbar.var>
# <xbar.var>string(VAR_OUTSIDE_US="False"): Set to "True" if you are outside the United States.</xbar.var>

# Todo: think about better error handling for missing data

import json, os
from datetime import datetime

try:
    from pydexcom import Dexcom, GlucoseReading
except:
    print("pydexcom not installed|color=red")
    print("---")
    print("Please run 'pip3 install pydexcom'.")
    exit()

# Get the Dexcom Share credentials from environment variables:
username = os.getenv('VAR_USERNAME', '')
password = os.getenv('VAR_PASSWORD', '')
if (os.getenv('VAR_OUTSIDE_US', '') == "True"):
    outside_US = True
else:
    # Note that we are defaulting to False if var is set to invalid value.
    outside_US = False

# Make sure we really got valid values:
if (username == '') or (password == ''):
    print("Set credentials|color=red")
    print("---")
    print("Open the xbar plugin browser to set your Dexcom Share login credentials.")
    exit()


# File for caching BG values
bg_filename = '/tmp/latest_bg_values.json'

def bg_values_to_file(bg_list, filename):
    '''Take a list of GlucoseReading objects, 
    serialize to JSON, and write to provided
    filename.'''

    # Handle the case with a single value for input: 
    if not isinstance(bg_list, list):
        iter_list = [bg_list]
    else:
        iter_list = bg_list
        
    try:
        with open(filename, 'w') as f:
            for b in iter_list:
                f.write(json.dumps(b.json)+"\n")
    except AttributeError:
        # If they have an old version of pydexcom, the
        # BG object won't have the 'json' property.
        # If we left behind an empty file, clean it up:
        if os.path.exists(filename): os.remove(filename)

            
def bg_values_from_file(filename):
    '''Given an input filename, read the 
    contents, assumed to be JSON serialized
    BG data from Dexcom Share.  Return a
    list of GlucoseReading objects.
    Assumes that checking for file 
    existence happens elsewhere. '''          
    
    # Reading from file
    b_list = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            # If valid JSON, try to create a GlucoseReading:
            json_data = json.loads(line)
            b_list.append(GlucoseReading(json_data))
            
    return b_list

        

now = datetime.now()
# See if we can get BG values from file:
have_old_bgs = False
# Did we get an exception when reading BGs:
read_exception = False
if os.path.exists(bg_filename):
    try:
        old_bgs = bg_values_from_file(bg_filename)
    except Exception as bg_read_exception:
        read_exception = bg_read_exception
    
    # Continue only if we successfully read:
    if (not read_exception) and (len(old_bgs) > 2):
        have_old_bgs = True
        bg_age = now - old_bgs[0].datetime
        bg_age_minutes = bg_age.total_seconds()/60
    
if have_old_bgs and (bg_age_minutes < 4):
    # No need to fetch new bgs:
    bgs = old_bgs
else:
    # Fetch new data.
    dexcom = Dexcom(username, password, ous=outside_US)
    bgs = dexcom.get_glucose_readings(max_count=6)

# Cycle over list to print output; even for old
# BG data we are updating the age displayed: 
for i in range(len(bgs) - 1):
    bg = bgs[i]
    bg_diff = bg.value - bgs[i+1].value
    time_diff = now - bg.datetime
    time_diff_min = time_diff.total_seconds()/60
    print(f"{bg.value} ({bg_diff:+0d}) {bg.trend_arrow} ({time_diff_min:0.0f}m)")
    if i==0:
        # Separator to make earlier values appear in the submenu: 
        print("---")

# If we encountered an exception when reading BGs, flag it:
if read_exception:
    print(f"Failed to read BGs from {bg_filename}:|color=red")
    print(f"{read_exception}.|color=red")

# Save BG values to file if possible. If an
# exception is raised, flag it but exit normally,
# since this caching isn't essential for the script
# to work:
try:
    bg_values_to_file(bgs, bg_filename)
except Exception as e:
    print(f"Failed to write BGs to {bg_filename}:|color=red")
    print(f"{e}.|color=red")
