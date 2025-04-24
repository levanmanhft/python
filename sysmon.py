import subprocess
import os
import requests 
import json 
#date
status, date = subprocess.getstatusoutput("date '+%G/%m/%d %H:%M'")
print(date)

#cpu usage
status, cpu_usage = subprocess.getstatusoutput("""mpstat 1 1 | tail -n 1 | awk '{print 100-$NF}'""")


#number connection

status, connection = subprocess.getstatusoutput("netstat -ntu | awk '/^tcp/ {print $5}' | wc -l ")

# disk usage

status, disk_total = subprocess.getstatusoutput("""df -m | awk '$6=="/" {print $2}'""")
status, disk_used  = subprocess.getstatusoutput("""df -m | awk '$6=="/" {print $3}'""")
disk_usage = 100.0*float(disk_used)/float(disk_total)


# mem usage

status, mem_total = subprocess.getstatusoutput("""free -m | grep ^Mem | awk '{print $2}' """)
status, mem_used = subprocess.getstatusoutput("""free -m | grep ^Mem | awk '{print $3}' """)
mem_usage = 100.0*float(mem_used)/float(mem_total)

# log processing
cpu_usage += '%'
disk_usage = f"{float(disk_usage):.2f}% (total {float(disk_total)/1024:.2f}GB)"
mem_usage = f"{float(mem_usage):.2f}% (total {float(mem_total)/1024:.2f}GB)"



logdir = '/var/log/clomon'
logpath = os.path.join(logdir, 'clomon.log')
if not os.path.exists(logdir):
    os.makedirs(logdir, exist_ok= True)
with open(logpath, 'a+') as file:
    if file.read() != '':
       file.write('\n')
    file.write('LOG_DATE:'+date+' | CPU_USAGE:'+cpu_usage+' | CONN_NUMBER:'+connection+' | DISK_USAGE:'+disk_usage+' | MEM_USAGE:'+mem_usage + '\n')


# send to slack cpu , mem , disk usageusage

slack_token = "xoxb..."
channel_id = "C084..."

headers = {
    "Authorization": "Bearer " + slack_token,
    "Content-Type": "application/json"
}

cpu_value = float(cpu_usage.replace('%', ''))
mem_value = float(mem_usage.split('%')[0])
disk_value = float(disk_usage.split('%')[0])
message = f""" 
               date : {date},
               cpu_usage : {cpu_usage},
               connection : {connection},
               disk_usage: {disk_usage},
               mem_usage: {mem_usage}
"""
payload = {
        "channel": channel_id,
        "text" : message
    }
if cpu_value >= 80 or int(connection) > 5000 or disk_value > 90 or mem_value > 80 :
        response = requests.post("https://slack.com/api/chat.postMessage", headers = headers, data = json.dumps(payload))
