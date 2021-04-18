# SiamSlim

**SiamSlim** implements a real-time single object tracking algorithm wchich can be deployed on board of UAVs, as presented in our [paper](https://jingyan.baidu.com/article/fa4125ac0013d328ac70922f.html) . The code based on the [PySOT](https://github.com/STVIR/pysot) and [SiamBAN](https://github.com/hqucv/siamban)

 We deploy the Siamese tracker on the UAVs, and then conduct flight tests on the outskirts of Beijing, China. Some images recorded in the flight test are shown in these figures. In various scenes and illumination conditions, our Siamese tracker tracks the objects smoothly. The pan tilt rotates by the directing of the tracker, to make the target near the image center.
<div align="center">
  <img src="demo/car.gif" width="200px" />
  <p>Example 1.</p>
</div>
A demo of the application of Siamese tracker on the UAVs. Based on the proposed Siamese tracker, we make a program of two UAVs accompanying flight. One UAV flies at random and another follow it by directing of Siamese tracker. Images on the first row are the first perspective of the following UAV and images on the second row are the third perspective captured from the ground.

In the first row, a person is tracked as he runs in random directions. In this process, the aspect ratio of the target changes accordingly and the tracker tackles the challenge. In the second row, a car with a high speed (about 60 km/h ) is tracked. In this process, the scale of the target changes accordingly and the tracker tackles the challenge. In the third row, a car is tracked under low illumination. The tracker tackles the partial occlusion challenge and prompts the user that the target is lost when the target is fully occluded.
