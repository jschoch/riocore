from riocore.plugins import PluginBase


class Plugin(PluginBase):
    def setup(self):
        self.NAME = "quadencoderz2"
        self.VERILOGS = ["quadencoderz2.v"]
        self.PINDEFAULTS = {
            "a": {
                "direction": "input",
                "invert": False,
                "pullup": False,
            },
            "b": {
                "direction": "input",
                "invert": False,
                "pullup": False,
            },
            "z": {
                "description": "index pin",
                "direction": "input",
                "invert": False,
                "pullup": False,
            },
        }
        self.OPTIONS = {
            "quad_type": {
                "default": 2,
                "type": int,
                "min": 1,
                "max": 4,
                "description": "encoder type",
            },
            "scale": {
                "default": 1,
                "type": int,
                "description": "ppr of the encoder",
            }
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
            "idx": {
                "size": 1,
                "direction": "input",
            },
            "raw_a": {
                "size": 1,
                "direction": "input",
            },

           "raw_b": {
                "size": 1,
                "direction": "input",
            },



        }
        self.SIGNALS = {
            "indexenable": {
                "is_index_enable": True,
                "direction": "inout",
                "bool": True,
            },
            "idx":{
                "direction": "input",
                "bool": True,
            },
            "raw_a":{
                "direction": "input",
                "bool": True,
            },
            "raw_b":{
                "direction": "input",
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
                    "rps": "value_rps = (raw_value - last_raw_value) * *data->duration / scale;",
                    "rpm": "value_rpm = (raw_value - last_raw_value) * *data->duration * 60.0 / scale;",
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
        self.INFO = "quadencoder with index pin"
        self.DESCRIPTION = ""

    def gateware_instances(self):
        instances = self.gateware_instances_base()
        instance = instances[self.instances_name]
        instance_predefines = instance["predefines"]
        instance_parameter = instance["parameter"]
        instance_arguments = instance["arguments"]
        quad_type = self.plugin_setup.get("quad_type", self.OPTIONS["quad_type"]["default"])
        instance_parameter["QUAD_TYPE"] = quad_type
        return instances
