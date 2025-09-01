from extras.scripts import Script
import requests
import json
import base64
import time


class CustomEventHandler(Script):
    class Meta:
        name = "Custom ONTAP NAS Event Handler"
        description = "Script to handle custom ONTAP NAS events in NetBox"

    def run(self, data, commit):
        # Process the event data
        # nas_name = data.get('name', {})
        # nas_tenant = data.get('tenant', {})
        
        with open('/opt/netbox/netbox/scripts/awx_config.json') as config_file:
            config_data = json.load(config_file)
            awx_username = config_data['awx_username']
            awx_password = config_data['awx_password']
            awx_instance = config_data['awx_instance']
            input_username = config_data['input_username']
            input_password = config_data['input_password']
            input_cluster = config_data['input_cluster']

        # Job template ID and extra vars
        job_template_id = '8'
        extra_vars = {
            'payload_data': data,
            'input_username': input_username,
            'input_password': input_password,
            'input_cluster': input_cluster
        }

        # Encode username and password for Basic Authorization
        auth_header = base64.b64encode(f'{awx_username}:{awx_password}'.encode()).decode('utf-8')
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/json'
        }

        # Make the POST request to launch the job template with extra vars
        launch_job_url = f'{awx_instance}:8043/api/v2/job_templates/{job_template_id}/launch/'
        launch_payload = {
            'extra_vars': json.dumps(extra_vars)
        }
        response = requests.post(launch_job_url, headers=headers, json=launch_payload, verify=False)

        # Check the response
        if response.status_code == 201:
            print("AWX Job launched successfully!")
            job_url = response.json()['url']
            print("AWX Job URL:", job_url)

            # Retrieve job status
            job_status = 'running'
            while job_status == 'running':
                job_response = requests.get(f'{awx_instance}:8043{job_url}', headers=headers, verify=False)
                job_status = job_response.json()['status']
                print("Job Status:", job_status)
                if job_status == 'successful' or job_status == 'failed':
                    break
                time.sleep(10)  # Check job status every 10 seconds

        else:
            print("Failed to launch AWX job. Status code:", response.status_code)
            print("Response:", response.json())
        

        # Extract relevant information from the event data
        

        # Call AWX instance job template using the extracted data
        # Insert your code here to make the API request to AWX
        self.log_info('NAS Script execution completed!')

        # Return a message indicating the script has run successfully
        #return '\n'.join([f"NAS name: {nas_name}, Tenant: {nas_tenant}, AWX Job result: {job_status}"])
        return '\n'.join([f"AWX Job ID: {job_url.split('/')[-2]}, AWX Job result: {job_status}"])
