A list of common questions and answers for using riocore


#### Q: What is the status of the project?

> Migrating from the old linuxcnc-rio project is currently in progress and testing is ongoing, however it is not ready for production use

#### Q:  Where can I get help?

> Use the discussion section of this repo

#### Q:  What is this project?

#### Q: How do I get started?

#### Q:  How do I create a test configuration?
1. Create a basic config, or copy an example from the riocore/configs directory

```
{
  "name": "basic_starting_point",
  "description": "Tangoboard with TangNano9K over SPI",
  "boardcfg": "TangNano9K",
  "protocol": "UDP",
  "plugins": []
}

```

2. Launch rio-setup
> If you are using venv you may run something like this `PYTHONPATH=. bin/python3 ../riogui/bin/rio-setup  test.json`
4. TODO: what is the minimum working config to be able to 1: start the test-gui?  2: start linuxcnc? 

#### Q: How do I setup a joint?

#### Q: How do I setup an MPG encoder?

#### Q:  How do I setup a lathe?

#### Q:  How do I setup a spindle encoder?

#### Q: 

#### Q: 

#### Q: 

#### Q: 

#### Q: 

#### Q: 

#### Q: 


