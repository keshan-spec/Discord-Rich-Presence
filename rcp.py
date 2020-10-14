from pypresence import Presence
import time

class RichPressence:
    def __init__(self, client):
        self.rpc = Presence(client)  # Initialize the client class
        self.rpc.connect()  # Start the handshake loop

    def set_presence(self, state, detail, large_image=None, starttime=None, limit=5):
        try:
            # while  True:
            if large_image and starttime:
                self.rpc.update(state=state, large_image=large_image, start=starttime, details=detail)  # Set the presence
            elif large_image:
                self.rpc.update(state=state, large_image=large_image, details=detail)  # Set the presence
            elif starttime:
                self.rpc.update(state=state, start=starttime, details=detail)  # Set the presence
            else:
                self.rpc.update(state=state, details=detail)  # Set the presence
                
                # time.sleep(limit)
        except Exception as e:
            print(e)
            self.rpc.close()  # close connection
            exit()

    def quit(self):
        try:
            self.rpc.close()  # close connection
        except Exception as e:
            print(e)
            pass
