import ctypes

ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
input('{Press enter to exit}')
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
