from flask import Flask, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)
output = []
with open('/var/log/apache2/access.log', 'r') as f:
    for line in f:
        fields = line.split()
        ip_address = fields[0]
        request_time = fields[3][1:]
        output.append({"ip_address": ip_address,
                       "request_time": request_time})

with open('access.json', 'w') as f:
    json.dump(output, f)

@app.route('/logs', methods=['GET'])
def get_logs():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    ip_address = request.args.get('ip')
    filtered_logs = []
    for log in output:
        log_datetime = datetime.strptime(log['request_time'], '%d/%b/%Y:%H:%M:%S')
        if start_date and log_datetime < datetime.strptime(start_date, '%d/%b/%Y:%H:%M:%S'):
            continue
        if end_date and log_datetime > datetime.strptime(end_date, '%d/%b/%Y:%H:%M:%S'):
            continue
        if ip_address and log['ip_address'] != ip_address:
            continue
        filtered_logs.append(log)
    return jsonify(filtered_logs)

if __name__ == '__main__':
    app.run()

    