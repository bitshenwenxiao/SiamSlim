# SiamSlim

**SiamSlim** implements a real-time single object tracking algorithm wchich can be deployed on board of UAVs, as presented in our paper (the link of paper will be updated after publication). The code is based on the [PySOT](https://github.com/STVIR/pysot) and the [SiamBAN](https://github.com/hqucv/siamban).

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




