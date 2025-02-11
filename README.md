**OBS Studio | Window Capture FIX**

This utility is based on Python and allows you to create a non-existent display for OBS Studio.

**Introduction**

Recently, I encountered a small but significant problem. My task was to record an application window through OBS Studio. The program itself already has this function, but it has a critical drawback: the window being recorded must remain active at all times. If we minimize or close the window, then OBS stops recording, which is extremely inconvenient.

My utility, **Window Capture FIX**, allows you to bypass this limitation. It creates a virtual display that OBS can use, enabling the captured window to be minimized or closed without interrupting the recording process. This is particularly useful for those who need to record applications that require frequent switching or minimizing windows.

**How it Works**

1. The utility establishes a virtual display that is not visible on the physical screen.
2. OBS Studio is configured to utilize this virtual display for capturing windows.
3. The window to be recorded can be minimized or closed, and the recording continues uninterrupted. The window is essentially moved to an invisible area, allowing the recording to proceed seamlessly.

**Development Process**
08/02/25, Version 1.0 was uploaded to GitHub.

09/02/25 Version 1.0 The recorded window is no longer minimized, even if all other windows are minimized.

10/02/25 Version 1.0 is inconvenient to use.

11/02/25 When using version 1.0, there are problems with the image freezing, because the recorded windows go into sleep mode.

12/02/25 The first build has been uploaded
