#Just a file that we can use globally to define weights and stuff, since changing/tuning them manually is annoying

# weights in order of [lines(+), height(-), holes(-), bumpiness(-),     max height(-)]
DEFAULT_WEIGHTS =     [   1.0  ,  -0.5,      -3.5,       -0.8,            -0.7       ]
#Positive means you want more of, negative means avoid states with those
#so like, in default, the AI will avoid holes more, since its larger negative value affects the overall evaluation more


#Below we can add other weight presets for fine-tuning:

#Preset 2 = []
#Preset 3 = []