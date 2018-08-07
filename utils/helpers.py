from time import time

def precise_sleep(duration, current_time=None):
        """
        sleep for number of seconds with the current time given
        Necessary for microsecond precise sleep 
        """
        if current_time:
            end = current_time + duration
        else:
            end = time() + duration
        while time() - end < 0:
            pass
        return True