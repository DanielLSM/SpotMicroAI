## SpotMicroAI for JetsonNano

The Nano will use a 16 Channel PCA9685 I2C-Servo Driver to drive the 12 Servos for the Legs.
First of all all prepare your Jetson Nano as you see in the NVIDIA Documentation.

Then connect to it via SSH and:

```
git clone https://github.com/FlorianWilk/SpotMicroAI.git
cd SpotMiroAI/JetsonNano
sudo apt-get install python3 python3-pip
pip3 install -U -r requirements.txt 
python3 start_robot.py
```