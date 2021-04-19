# SiamSlim

**SiamSlim** implements a real-time single object tracking algorithm wchich can be deployed on board of UAVs, as presented in our paper (the link of paper will be updated after our paper publication). The code is based on the [PySOT](https://github.com/STVIR/pysot) and the [SiamBAN](https://github.com/hqucv/siamban).

We deploy the Siamese tracker on the UAVs, and then conduct flight tests on the outskirts of Beijing, China. Some images recorded in the flight test are shown in these figures. In various scenes and illumination conditions, our Siamese tracker tracks the objects smoothly. The pan tilt rotates by the directing of the tracker, to make the target near the image center.
<div align="center">
  <img src="demo/5.gif" width="320px" />
  <img src="demo/6.gif" width="469px" />
  <p>Example 1.</p>
</div>

Example 1 shows a demo of the application of Siamese tracker on the UAVs. Based on the proposed Siamese tracker, we make a program of two UAVs accompanying flight. One UAV flies at random and another follows it by directing of Siamese tracker. Images on the left figure are the first perspective of the following UAV and images on the right figure are the third perspective captured from the ground.
<div align="center">
  <img src="demo/3.gif" width="260px" />
  <img src="demo/2.gif" width="260px" />
  <img src="demo/4.gif" width="260px" />
  <p>Example 2.</p>
</div>


In the left figure, a person is tracked as he runs in random directions. In this process, the aspect ratio of the target changes accordingly and the tracker tackles the challenge. In the middle figure, a car with a high speed (about 60 km/h ) is tracked. In this process, the scale of the target changes accordingly and the tracker tackles the challenge. In the right figure, a car is tracked under low illumination. The tracker tackles the partial occlusion challenge and prompts the user that the target is lost when the target is fully occluded.

# Results

The raw results are in "./result/"

# Train or test on PC

If you want to train or test on PC, please use the code in "./on_PC/". The code is based on the [PySOT](https://github.com/STVIR/pysot) and the [SiamBAN](https://github.com/hqucv/siamban)

## Webcam demo on PC
```bash
cd on_PC
python cam.py
```

# Test on TX2

In order to deploy on TX2 conveniently, we compile the tracker into ".so" format library on TX2. If you want to test on TX2, please use the code in "./on_TX2/". 

## Webcam demo on TX2
```bash
cd on_TX2
python cam.py
```




