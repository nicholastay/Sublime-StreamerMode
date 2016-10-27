# Sublime-StreamerMode (for Sublime Text **3**)

*(I apologize in advance for the cringey sellout message)*

Do you stream programming and worried/have accidentally opened config files or the like with confidential data? Well, this plugin is the plugin for you.

## Install
Available on Package Control (still being processed at the time of commit, but should be OK soon™)

Manual install:
```
$ cd /Users/nicholastay/Library/Application Support/Sublime Text 3/Packages # or where your packages are
$ git clone https://github.com/nicholastay/Sublime-StreamerMode.git

# Tested with Sublime Text 3, build 3114.
```


## Usage
* Open Sublime Text and open the Command Palette and use 'Streamer Mode: Toggle'.
* Open your Preferences (User) and add glob patterns to the hide list - access to those files will be hidden while streamer mode is active.
* Toggle streamer mode with that Command Palette option.
* When a restricted file is open you can use the Command Palette on that page and select 'Streamer Mode: Override' to force open the file.


## Important Note(s)
* While Streamer Mode is active, you should **not** modify the `binary_file_patterns` prop in the user preferences. This is modified by Streamer Mode to hide your confidential files from the 'Goto Anything' menu and 'Find in Files'. You can, however, modify it while Streamer Mode is disabled.


## Contributing
Contributions are highly valued, welcomed and appreciated whether it is just to file an Issue, or to even make a Pull Request. This is my first Sublime Text plugin as well as my first time using Python in a long time.
For Pull Requests, please direct them to the `dev` branch, thanks.