## Developer Documentation

### Considerations

Because there are so many interrelated components and dependencies on LCNC development cycles can be very slow.

You must get into the habbit of re-generating everytime you update a plugin or it's verilog.

# Definitions

Module: TODO: Oliver?
Plugin:
Signal:
Net: 
Interface: 
Gateware Instance:

## Modify Plugin

If you want to modify a plugin and add a raw signal for an input you first need to edit the plugin's python script.  First choose a name, let's say "raw_a".  You need to add a section in self.INTERFACE, and self.SIGNALS for this data.

```
        self.INTERFACE = {
            
            "idx": {
                "size": 1,
                "direction": "input",
            },
            "raw_a": {
                "size": 1,
                "direction": "input",
            },

        }
        self.SIGNALS = {
            
            "idx":{
                "direction": "input",
                "bool": True,
            },
            "raw_a":{
                "direction": "input",
                "bool": True,
            },

```


Then you need to add it to the verilog module interface and update the value.

```
// in the module interface
output reg idx = 0,

...

// put some data in the reg
always @(posedge clk) begin
        idx <= z;
        raw_a <= a;

```

