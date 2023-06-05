# Nreal for IoT
<details><summary> May 26, 2023 : Regarding Nreal to Change Name of Company to "Xreal"</summary>

Nreal Japan, a developer and seller of augmented reality (AR) glasses, announced on May 26 that it will change its company name and brand name.  
From now on, "Nreal" will be developed as "XREAL," and after May 25, the respective names will be as follows  
* Company name : Japan Xreal Co. (formerly Japan Nreal Co., Ltd.)
* Brand name : XREAL (formerly Nreal)
* Official website URL: https://www.xreal.com/jp (Formerly https://www.nreal.jp/)
* Product name
  * XREAL Air (Formerly Nreal Air)
  * XREAL Adapter (formerly Nreal Adapte)
  * XREAL Light (Formerly Nreallight)

</details>
 
## Summary of IoT for Nreal
<img src="https://i.ebayimg.com/thumbs/images/g/HzgAAOSwSgdiaRQp/s-l1600.jpg" alt="NrealAir_logo" width="120px"><img src="https://i.ebayimg.com/thumbs/images/g/qkgAAOSwKzViSArn/s-l1600.jpg" alt="NrealAir_logo" width="120px">

This project aims to visualize the sensor information of the surroundings using "Nreal Ari," which was released on March 4, 2022.

## Specific Approaches
A device called ReSpeaker Mic Array v2.0 is used to detect the direction of sound. This device can be used as long as it can be powered via USB, and we will connect it to Raspberry Pi to measure the sound.
Nreal is connected to a Raspberry Pi micro-HDMI via a dedicated Nreal converter to enable screen output.

## Implementation Features
- Sound Direction Detection and Corresponding Object Generation
Using Python's "Pygame", we implemented a function to generate an arrow-like object from the direction of the detected sound.

![flyobj_gif](https://github.com/TakumiSenaha/Nreal_IoT/assets/117294735/f89f26a6-0843-4879-88d4-d085f5a7c01a)

---

- Speech Recognition and Text Display
Speech recognition using "SpeechRecognize" in Python. 

![textobj_gif](https://github.com/TakumiSenaha/Nreal_IoT/assets/117294735/996486ca-1ef3-44a2-b5fb-471adcd80d04)

---

- Transition Mode Using Touch Sensor
The touch sensor enables switching to object generation mode, switching to text display mode, and switching recognition languages.

![demo_flyobj_PC_gif](https://github.com/TakumiSenaha/Nreal_IoT/assets/117294735/a20b2134-7b38-4e1e-a949-e3b419f07e95)
![demo_textobj_PC_gif](https://github.com/TakumiSenaha/Nreal_IoT/assets/117294735/e6e67482-6b7b-487c-b770-9161dbca091b)

---

## Demo on Nreal

![flyobj_onNreal_gif](https://github.com/TakumiSenaha/Nreal_IoT/assets/117294735/1fc57f90-bf97-4d54-aac5-bde312461910)
![textobj_onNreal_gif](https://github.com/TakumiSenaha/Nreal_IoT/assets/117294735/83070ae5-8773-4219-9730-440085a45506)

---

# Installation
```bash
git clone 'this repo'
cd Nreal_IoT
sudo pyhton3 main.py
```
It is assumed to be run with administrator privileges and with python3 series. Depending on your environment, there may be libraries to install.

## Technology Used
* Pyhton
* Nreal
* ReSpeaker Mic Array v2.0
* Raspberry Pi

# References
## For ReSpeaker Mic Array v2.0
```bash
git clone https://github.com/respeaker/usb_4_mic_array.git
cd usb_4_mic_array
```
The sensor information such as voice direction is acquired by importing the information in the code "tuning.py" in this file.
Then, create a DOA.py with below code under usb_4_mic_array folder and run 'python DOA.py'For details, please refer to the following URL.

https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/#vad-voice-activity-detection

## For Touch Sensor (TTP223B Module Sensor)
For the touch sensor, refer to the following OSOYOO site for code implementation.
https://osoyoo.com/ja/2017/03/24/%e5%9f%ba%e4%ba%8e%e6%a0%91%e8%8e%93%e6%b4%be%e7%9a%84%e8%a7%a6%e6%91%b8%e5%bc%80%e5%85%b3/

Example
```bash
sudo wget http://osoyoo.com/driver/touchsensor.py
sudo python ./touchsensor.py
```
