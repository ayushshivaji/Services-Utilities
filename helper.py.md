```python helper.py
import pyautogui
import time
import sys

pyautogui.PAUSE = 0  # or a smaller delay like 0.01
# Give you 2 seconds to switch to the tmux window
# Press Ctrl + Space
pyautogui.keyDown('ctrl')
pyautogui.press('space')
pyautogui.keyUp('ctrl')
pyautogui.press('`')

# Short pause
# time.sleep(0.1)

# Press 'x'

command = sys.argv[1]
if command == 'dl':
    pyautogui.typewrite('docker logs -f --tail 100 ')
pyautogui.typewrite('hello', interval=0.00001)
```