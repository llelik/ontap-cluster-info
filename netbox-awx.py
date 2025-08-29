from extras.scripts import Script

class CustomEventHandler(Script):
    class Meta:
        name = "Custom ONTAP NAS Event Handler"
        description = "Script to handle custom ONTAP NAS events in NetBox"

    def run(self, data):
        # Process the event data
        event_data = data.get('event', {})
        
        # Extract relevant information from the event data
        key1 = event_data.get('key1')
        key2 = event_data.get('key2')

        # Call AWX instance job template using the extracted data
        # Insert your code here to make the API request to AWX

        # Return a message indicating the script has run successfully
        return f"Script executed successfully with key1: {key1}, key2: {key2}"

