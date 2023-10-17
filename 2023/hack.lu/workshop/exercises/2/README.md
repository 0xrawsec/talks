# BPFDoor Malware Sample

Assuming you are a detection engineer and you want to build
one or more detection rules to catch BPFDoor malware. 

Imagine a methodology which could help you doing so ? Share it with others :)

# Tips to run BPFDoor
* run the sample with sudo otherwise it won't work
* the malware checks if an instance already running. So if you ran it already once you'll need to delete a file before running it again. Look at the source code in `BPFDoor/bpfdoor.c` for a file to delete (ask if not sure).

# Going Further (homework)

1. reverse engineer the malware and find the password it needs
2. write a program to send commands to it
3. apply your methodology and build new rules