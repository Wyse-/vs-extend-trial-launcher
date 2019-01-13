# vs-extend-trial-launcher
This script will extend the trial of Visual Studio Community 2017 and launch it. The default number of days which will be added to the trial is 31, which is the maximum allowed on version 15.9.4.

As to why you would want to use this: personally I use it because I don't want to keep a Microsoft account logged in into Visual Studio just to use it, which I assume is just required for datamining purposes. This is also the only way I know of using Visual Studio fully offline for an undefined time: you would think that logging into an account once, or using the license file of a previously logged in account since that is also possible, and going offline would solve the problem, but apparently licenses go "stale" after a while.

Based on (this Stackoverflow answer)[https://stackoverflow.com/a/51570570].

## Requirements
- Python 3.x
- pywin32 (run `pip install pywin32`)
- Visual Studio Community 2017 in trial mode

## Usage
Just download the python file from this repository and use it to launch Visual Studio (i.e. change your shortcut(s) from devenv.exe to this script). If your Visual Studio installation directory is different than the default edit the `DEVENV_EXECUTABLE_PATH` constant value in the script.

The script will flash the cmd window background to green if everything goes well, red if an exception occurred, so you should be able to tell at a glance if it worked.
