## Dexcom menubar

This Python script is a plugin for [xbar](https://xbarapp.com/) that allows you to pull recent blood glucose values from [Dexcom Share](https://www.dexcom.com/training-videos/setting-up-dexcom-share-and-follow) and display them in the Mac menubar:

![Image of BG value in menubar](Dexcom_BG_screenshot.png)

The design is based heavily on the [Nightscout](https://github.com/nightscout/cgm-remote-monitor#nightscout-web-monitor-aka-cgm-remote-monitor)-based menubar apps by [Mark Wilson](https://github.com/mddub/nightscout-osx-menubar) and [Michael Pangburn](https://github.com/mpangburn/NightscoutMenuBar). 

### Prerequisites:

* A working Python 3 installation.  While Python is no longer included by default with the Mac OS, you can install it from the Xcode command-line tools, [homebrew](https://brew.sh/), or [Anaconda](https://www.anaconda.com/).
* The [pydexcom](https://github.com/gagebenne/pydexcom) package.  Install it with `pip3 install pydexcom`. 
* A working Dexcom Share setup that is uploading your blood glucose values (or those of someone who has given you access to their data) to the cloud. 

### To install: 

I hope to submit this to the repository of xbar plugins, but until then: 

* Copy the [Dexcom_BG.1m.py](Dexcom_BG.1m.py) script to `~/Library/Application Support/xbar/plugins/`.
* Set your Dexcom Share username and password via accessing the plugin in the xbar interface, or by editing the script directly and changing `VAR_USERNAME` and `VAR_PASSWORD`. 
* Optionally, set `VAR_OUTSIDE_US` to "True" if you are not in the United States. 

Enjoy! If you have any questions or problems, please open an issue here. 


