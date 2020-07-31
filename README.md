# Implementation of ITU-T Recommendation G.1072 

This repo provides the implementation of ITU-T G.1072 "Opinion model predicting gaming quality of experience for cloud gaming services" based on network and comperession parameters. 

- The G.1072 Planning model can predict the cloud gaming video quality based on the video paramters, bitrate, framerate, encoding resolution, gaming video complexity and network parameters, packetloss, delay. 

## How to Use
In order to run the code please use run it based on the parameters of the model as follows:

- Test the model based on the parameters, which requires specifying all video parameters, bitrate, framerate, ecoding resolution (width x height,e.g. 1920x1080) and video complexity (Vcomplexity) level ('High','Medium' ,'Low') and network parameters packetloss (if freezing is the effect), packetlossUDP (if slicing is the packet loss effect), delay and delay (interaction) complexity (Icomplexity) .  To do so, you can run it as the following example:

```
    python G1072.py --bitrate=50  --framerate=60  
                    --packetloss=0 --packetlossUDP=0 
                    --delay=400 --coding_res=1920x1080  
                    --Icomplexity=High --Vcomplexity=High  
                    --test_type=parameters
```

 For more help run:
 ```
    python test.py -h
```

### Application Range of Parameters 

Please note that the model only works based on the range of parameters used for training the model. 
- Bitrate: 0.3 kbps to 50 Mbps
- Framerate: 10 fps to 60 fps
- Resolution: 1920x1080, 1280x720 or 640×480
- Video Complexity Class: High, Medium, Low
- Interaction Sensitivity Class: High, Medium, Low
- Packetloss (Freezing effect): 0 - 0.5
- Packetloss (Slicing effect): 0 - 0.5
- Delay: 0 - 400


### Output of the model
The model gives you four estimations: 
- Overall Quality
- Interaction Quality (known as Input Quality in G,1072)
- Video Fragementation (based on https://github.com/stootaghaj/GamingVQA)
- Video Unclearness (based on https://github.com/stootaghaj/GamingVQA)

#### Example 
 ```
    python G1072.py --bitrate=50  --framerate=60  
                    --packetloss=0 --packetlossUDP=0 
                    --delay=400 --coding_res=1920x1080  
                    --Icomplexity=High --Vcomplexity=High  
                    --test_type=parameters
 ```
Output: 

 ```
    ('Overal Quality:', 4.582801247415103)
    ('Quality of Interaction Quality:', 4.6229955301830845)
    ('Video Unclearness:', 4.607621778600887)
    ('Video Fragmentation:', 4.471200161599724)
 ```

# Prepration 
Install python and pip, if they are not already installed. Follow the platform specific installation instructions. The following step should be performed to prepare the setup.
```
    git clone https://github.com/stootaghaj/ITU-G1072.git 
    pip install -r requirements.txt
```


## Citation 
Please cite the ITU-T Recommendation G.1072 if you use the code or to get more insight about the model:
```
    @inproceedings{g1072,
    title={ITU-T Recommendation G.1072: Opinion model predicting gaming quality of experience for cloud gaming services},
    booktitle={International Telecommunication Union},
    year={2019},
    organization={ITU}
    }
```

Link to ITU-T Recomendation G.1072: https://www.itu.int/rec/T-REC-G.1072-202001-I/en

## Contributors 

The work has been done within the ITU-T Study Group 12 under work item, G.OMG. Many researchers contributed to this work from TU Berlin, Simula Research Lab, Kingston University, Deutsche Telekom.
The current code is made available to test the model. It has to be noted that code is different than the original code and might include bugs. Please contact saman.zadtootaghaj@qu.tu-berlin.de if any issues is found. 

Saman Zadtootaghaj
Steven Schmidt 
Saeed Shafiee Sabet
Nabajeet Barman

## License 

For a commercial license, you must contact the respective rights holders of the standards ITU-T Rec. G.1072, ITU-T Rec. G.1071. 

Permission is granted, free of charge, to use the software for non-commercial research purposes.

