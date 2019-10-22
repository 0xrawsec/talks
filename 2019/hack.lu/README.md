# Introduction to WHIDS an Open Source Endpoint Detection System for Windows 

## Outline

1. Introduction to WHIDS
2. WHIDS Installation and feature exploration
3. Writing rules: methodology and practical exercises
4. Putting everything together: one case study of your choice will be given to you and the objective will be to write your own rule(s)

The workshop will be in four parts, trying to put the focus on hands-on.
After this workshop, the attendees will be able to:

 * Deploy and configure WHIDS
 * Interpret alerts and file dumps
 * Write custom detection rules
 * Use helper tools like [Gene](https://github.com/0xrawsec/gene)

## Materials

* One Windows 10 VM will be provided
* Tools and exercises will be provided at the time of the Workshop

## Pre-requesites

* a laptop which can run **a Windows 10 VM** with 2 cores and 4GB of RAM
* walk through [rules documentation](https://rawsec.lu/doc/gene/1.6/)
* knowing the basics about how to use [jq](https://stedolan.github.io/jq/) is recommended
* be familiar with [Sysmon](https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon) and what one can find in events. You can find a summary table over here [Sysmon Event Table](https://rawsec.lu/blog/posts/2017/Sep/19/sysmon-events-table/)

## Exercises

### Working on extracts

I have extracted some full WHIDS traces and the goal is to identify suspicious
events and create rules for those.

#### Exercise 1.1: Post-exploitation, access to a sensitive service

An attacker has gained access to your system and managed to elevate his privileges.
His goal is now to prevent you from receiving the logs of the machine.

**Q1**: There is one event in particular event which is typical of this technique. Hunt for it and create a rule (use of test flag operator would be appreciated).

#### Exercise 1.2: Maldoc has been run

A malicious document has been opened on the machine. 

**Q1**: Identify the dropper and build a rule for it. Do you have an idea why the dropper payload is not executed by WINWORD ?

**Q2**: Identify the drop sites and create a rule for it (create a container rule). 

#### Exercise 1.3: Executable malware has been run 

One of your colleague has received an email with a link.
He downloaded an executable and executed it.

#### Exercise 1.4: RAT

A machine has been compromised by a Remote Administration Tool malware.
The SOC also told you that the credentials of the user were used on an unusual machine.

**Q1**: Identify its persistence mechanism and create a rule for it.

**Q2**: Credential stealing is often done with accessing the memory of a specific service. Identify that event and create a rule to catch it (use of test flag operator would be appereciated).

**Q3**: Create rules matching the command lines executed by the RAT

#### Exercise 1.5: Reflective PE Loading (windows 7)

During an incident you have identified that a threat actor is using a particular
technique to inject code into a foreign process.

**Q1**: Identify the suspicious patterns and create rule(s) for it.

**Q2**: Can you imagine another implementation of this technique that would bypass the rules you have just created ? How ?

### Case Study:

Work on your own to create rules for malware or techniques.

The original idea was to make the participants bring their own malware / technique they want to create the rules for.

For the attendees who came without anything to work on, I have created some exercises.

#### Methodology for rule development

It is strongly advised to apply this methodology on a VM

1. Set up WHIDS so that it logs everything going through (option: `log-all`). Depending on how you want to work, you can make WHIDS forward the logs to a remote machine. Optional: you can also set the dump `mode` option to empty string if you don't want dumps to be created while you are developing rules. 
2. Reboot the machine to take the change into account
3. Optional: setup your working environment (shared drives, tools ...)
4. **Snapshot the VM**
5. Run the malware / technique you want to study
6. Dump the logs 
7. Develop the rules with the help of Gene. It's good to keep the traces you have worked on somewhere on your disk so that you can eventually rework on your rules later on.
8. Select your next target and revert to snapshot made in step 4

#### Exercise 2.1: Malware

Create rules to catch instances of that malware

#### Exercise 2.2: Malware

Create rules to catch instances of that malware

#### Exercise 2.3: Technique (process created with WMI)

A malware reverser (or you :)) found out a new technique used by a malware or an attacker.
You identified how to replicate this technique in a lab and you now want to create a rule allowing you to catch any use of this technique.

**Q1**: do you understand why this technique is interesting for attackers ?

**Q2**: do you remember a rule we have created earlier that would work to detect this technique ?

## Reference

* Microsoft Sysmon: https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon
* jq documentation: https://stedolan.github.io/jq/manual/
* Regex syntax used in Gene rules: https://github.com/google/re2/wiki/Syntax
* Gene Documentation: https://github.com/0xrawsec/gene-rules
* Repository of Gene rules: https://github.com/0xrawsec/gene-rules
