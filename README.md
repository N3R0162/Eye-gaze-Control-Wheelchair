## Eyegaze control wheelchairs
This is the eye gaze control code for the Capstone Project. It includes the implementation of GazeCaps: Gaze Estimation With Self-Attention-Routed Capsules [2] and I use the mapping method from eye gaze vector to computer screen by Webcam-based gaze estimation for computer screen interaction [1].

## Install requirements
To install the required library, please run:
```sh
pip install -r requirements.txt
```

## Running Procedure:
### Camera Calibration:
Because the default camera position is under the screen and it is inverted, if you want to run it normally on a webcam of a computer, which has the location on top of the screen, please run the calibration code with a 7x11 printed checker board. The command to run calibration is:

```sh
python3 ./camera_calibration.py
```

### Running the program:
To run the program, please run:

```sh
python3 ./src/main-pl.py
```

## Reference:
[1] Lucas Falch and Katrin Solveig Lohan, "Webcam-based gaze estimation for computer screen interaction", Frontiers in Robotics and AI, Volume 11 - 2024 | https://doi.org/10.3389/frobt.2024.1369566
[2] Wang, X., Wei, X., Li, Y., Deng, H., & Yu, Z. (2023). GazeCaps: Gaze Estimation With Self-Attention-Routed Capsules. IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)| https://openaccess.thecvf.com/content/CVPR2023W/GAZE/papers/Wang_GazeCaps_Gaze_Estimation_With_Self-Attention-Routed_Capsules_CVPRW_2023_paper.pdf
