# FAQ

## Q: what is required for lathe mode?

For non-sync movement you can just set the machine type value to lathe in riogui.

For threading you need a spindle encoder.

For G96 you need a spindle encoder and to also configure velocity feedback via `spindle.0.revs` and `spindle.0.speed-in`

example: 

```json
                        "indexenable": {
                            "net": "spindle.0.index-enable"
                        },
                        "position": {
                            "net": "spindle.0.revs",
                            "scale": 600
                        },
                        "rps": {
                            "net": "spindle.0.speed-in"
                        },

                        ```
