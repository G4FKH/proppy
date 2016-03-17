import datetime
import json
import urllib.request
import re

ssn_url = "ftp://ftp.ngdc.noaa.gov/STP/space-weather/solar-data/solar-indices/sunspot-numbers/predicted/table_international-sunspot-numbers_monthly-predicted.txt"
out_fn = 'ssn.json'

now = datetime.datetime.utcnow()
ssn_dict = {}
print ("Requesting file from {:s}".format(ssn_url))
response = urllib.request.urlopen(ssn_url)
data = response.read()
text = data.decode('utf-8')
print(text)
print ("Writing data to ssn.json")
ssn_pattern = re.compile('\s+(\d\d\d\d)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)')
for line in text.splitlines():
    print("Matching: *{:s}*".format(line))
    m = ssn_pattern.match(line)
    if m:
        year = m.group(1)
        print("Reading Year: {:s}".format(year))
        ssn_values = [m.group(2),
                    m.group(3),
                    m.group(4),
                    m.group(5),
                    m.group(6),
                    m.group(7),
                    m.group(8),
                    m.group(9),
                    m.group(10),
                    m.group(11),
                    m.group(12),
                    m.group(13)]
        print(ssn_values)

        for idx, ssn in enumerate(ssn_values):
            print('looping')
            if year not in ssn_dict:
                ssn_dict.update({year:{idx+1:ssn}})
            else:
                ssn_dict[year][idx+1] = ssn


with open(out_fn, 'w') as outfile:
    json.dump(ssn_dict, outfile)

print ("Saved to {:s}".format(out_fn))
