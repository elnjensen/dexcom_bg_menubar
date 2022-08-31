## Dexcom menubar

This Python script is a plugin for [xbar](https://xbarapp.com/) that allows you to pull recent blood glucose values from [Dexcom Share](https://www.dexcom.com/training-videos/setting-up-dexcom-share-and-follow) and display them in the Mac menubar:

![Image of BG value in menubar](Dexcom_BG_screenshot.png)

Prerequisites:

* A working Python 3 installation.  While Python is no longer included by default with the Mac OS, you can install it from the Xcode command-line tools, homebrew, or Anaconda.
* The pydexcom package.  Install it with `pip3 install pydexcom`. 
* A working Dexcom Share setup that is uploading your blood glucose values (or those of someone who has given you access to their data) to the cloud. 
