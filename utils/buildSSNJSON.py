import datetime
import json
import urllib.request

url = 'http://sidc.oma.be/silso/FORECASTS/prediSC.txt'
out_fn = 'ssn.json'

now = datetime.datetime.utcnow()
ssn_dict = {'comment':'Retreived {:s}'.format(now.strftime("%Y-%m-%d %H:%M"))}
print ("Requesting file from {:s}".format(url))
response = urllib.request.urlopen(url)
data = response.read()
text = data.decode('utf-8')
print(text)
print ("Writing data to ssn.json")
for line in text.splitlines():
    year = line[0:4]
    month = line[5:7]
    ssn = int(float(line[20:25]))

    if year not in ssn_dict:
        ssn_dict.update({year:{month:ssn}})
    else:
        ssn_dict[year][month] = ssn

with open(out_fn, 'w') as outfile:
    json.dump(ssn_dict, outfile)

print ("Saved to {:s}".format(out_fn))
