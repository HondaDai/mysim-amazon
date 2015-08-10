
from amazon import *

print status_all()

stop_all()
[ wait_state(i.tags['Name'], "stopped") for i in get_all_instances() ]
print "All Stopped."