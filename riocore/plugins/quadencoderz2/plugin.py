from riocore.plugins import PluginBase


class Plugin(PluginBase):
    def setup(self):
        self.NAME = "quadencoderz"
        self.INFO = "quadencoder with index pin"
        self.DESCRIPTION = (
            "usable as spindle-encoder for rigid tapping and thread cutting.  It is critical that your position-scale and QUAD_TYPE match, see the details in the description for QUAD_TYPE"
        )
        self.KEYWORDS = "feedback encoder rotary linear glassscale  index"
        self.ORIGIN = "https://www.fpga4fun.com/QuadratureDecoder.html"
        self.VERILOGS = ["quadencoderz.v"]
        self.PINDEFAULTS = {
            "a": {
                "direction": "input",
                "invert": False,
                "pull": None,
            },
            "b": {
                "direction": "input",
                "invert": False,
                "pull": None,
            },
            "z": {
                "description": "index pin",
                "direction": "input",
                "invert": False,
                "pull": None,
            },
        }
        self.OPTIONS = {
            "quad_type": {
                "default": 2,
                "type": int,
                "min": 0,
                "max": 4,
                "description": "The count from the encoder will be bitshifted by the value of QUAD_TYPE.  Use 0 for 4x mode.  The position-scale should match.  For examle if you have a 600 CPR encoder 4x mode will give you 2400 PPR and your scale should be set to 2400.",
            },
        }
        self.INTERFACE = {
            "indexenable": {
                "size": 1,
                "direction": "output",
            },
            "indexout": {
                "size": 1,
                "direction": "input",
            },
            "position": {
                "size": 32,
                "direction": "input",
            },
        }
        #  how do i get the signal_setup from the json?
        blob = """
    static FilterState filter_state = {0.0,0.0};
    // Higher alpha more responsive to position delta
    static float alpha = 0.2;
    // Higher beta more responsive to velocity changes
    static float beta = 0.01;
    float delta_counts = raw_value - last_raw_value;
    float duration = *data->duration;
    alpha_beta_filter(&filter_state,delta_counts,alpha,beta,duration,scale);
    value_rps = fabs(filter_state.velocity);

    // if RPS < 1RPM return 0
    if(value_rps < .016){
        value_rps = 0.0;
        }
    *data->SIGIN_QUADENCODERZ0_RPS = value_rps;
"""
        self.SIGNALS = {
            "indexenable": {
                "is_index_enable": True,
                "direction": "inout",
                "bool": True,
            },
            "indexout": {
                "is_index_out": True,
                "direction": "input",
                "bool": True,
            },
            "position": {
                "is_index_position": True,
                "direction": "input",
                "targets": {
                    "rps": blob,
                    "rpm": "value_rpm = value_rps * 60;",
                },
                "description": "position feedback in steps",
            },
            "rps": {
                "direction": "input",
                "source": "position",
                "description": "calculates revolutions per second",
            },
            "rpm": {
                "direction": "input",
                "source": "position",
                "description": "calculates revolutions per minute",
            },
        }

        self.last_pos = 0

    def gateware_instances(self):
        instances = self.gateware_instances_base()
        instance = instances[self.instances_name]
        instance["predefines"]
        instance_parameter = instance["parameter"]
        instance["arguments"]
        quad_type = self.plugin_setup.get("quad_type", self.OPTIONS["quad_type"]["default"])
        instance_parameter["QUAD_TYPE"] = quad_type
        return instances

    def convert(self, signal_name, signal_setup, value):
        if signal_name == "position":
            scale = self.plugin_setup.get("signals", {}).get(signal_name, {}).get("scale", 1.0)

            # calc rps/rpm
            if self.duration > 0:
                diff = value - self.last_pos
                rps = diff / self.duration / scale
                self.SIGNALS["rps"]["value"] = rps
                self.SIGNALS["rpm"]["value"] = rps * 60
            self.last_pos = value

            vmin = self.plugin_setup.get("min")
            vmax = self.plugin_setup.get("max")
            if vmin is not None and value < vmin:
                value = vmin
            if vmax is not None and value > vmax:
                value = vmax
            if scale is not None:
                value *= scale
        return value
