# Discovering the possibilities

## Kunai

Lets run the thing for a few minutes and see what info we can get.

```bash
# run kunai as sudo and pipe the output to a file (important)
# NB: jq is used here just to make a pretty json output
sudo kunai | jq '.' | tee /tmp/kunai.json

# make sure you run this command, it has no particular
# importance right now but we'll use it later in this exercise
/bin/ls -hail
```

Feel free to ask any question you want !

Let's take a quick look at the [events documentation](https://why.kunai.rocks/docs/category/kunai---events)

## kunai-search.py

Small script to help us searching into kunai-logs. It can be used for instance
to trace recursively all the activity of a task group (i.e. process).

NB: grep cannot be used (in an easy way) to track down processes recursively.
A lookup table needs to be updated along the way.

Let's use it quickly to understand how it works, we will need it in the next
exercise.

## Introduction to Gene

Repo: https://github.com/0xrawsec/gene

Gene is a tool and a rule format used to create detection/filtering
primitives on any kind of logs. The command line utility only supports two
kinds of inputs EVTX and json. On the other hand the API can be bended in
such a way that any kind log can be matched against rules.

1. open `simple-rule.gen` in a text editor (vscodium in VM)
2. lets explain briefly the format (that's my job :))
3. apply the rule on the file we've used to dump kunai output 

```bash
# make sure you've run one or more times /bin/ls -hail
# as requested in the previous section
gene -r simple-rule.gen -j /tmp/kunai.json
```

### Important points to remember about rules

* Criticality will be used to score the criticality of an event matching the rule(s). Score cannot be higher than 10. The higher the score the more critical
the event is. 
* Meta.Events section is used to **speed up** rule matching so always try to use it. It is used to match event ids
* Matches section may contain absolute or relative (to data section) field path
* the data section is not the same for all events (/info/data for kunai events, /Event/EventData for Windows events)

## Let's build the cheapest detection system you've ever seen

It is as complicated as using a pipe

```bash
# voilà
# NB: piping to jq is not mandatory it is just there to make a pretty output
sudo kunai | gene -r simple-rule.gen -j - | jq '.'
```

In another terminal

```bash
# our rule matches the execution of this exe/command line
/bin/ls -hail
```

Go back to Kunai terminal and see the result

# Going Further (homework)

Explore a bit more [gene](https://github.com/0xrawsec/gene) and its rule format

