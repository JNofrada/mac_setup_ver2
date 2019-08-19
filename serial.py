import subprocess
task = subprocess.Popen(['system_profiler', 'SPHardwareDataType'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = task.communicate()

for l in out.split('\n'):
	if 'Serial Number (system):' in l:
		serial_line = l.strip()
		break

serial = serial_line.split(' ')[-1]

print (serial)