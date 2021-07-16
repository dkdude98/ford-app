# GarageBuddy - Ford Smart Car Connectivity Challenge

To run the code, there is no need to download the repository. Please visit: https://ford-iot-app.herokuapp.com/
A video demo can be found here: https://www.youtube.com/watch?v=Ou590cjRz3c

You will need a MyQ Smart Garage Hub to experience all functionalities, as well as a Ford internet connected vehicle. The 24/7 Python backend however, is not running currently
to avoid incurring charges.

Steps:
* Visit the account creation page, make an account, and log in.
* Login to your Ford account and indicate the VIN of the car which you would like to use. Save these credentials in the app.
* Login to your MyQ account, save the credentials, and select the garage you would like to make use of.
* Using the map, mark the location of your garage and save the location.
* Finally, click the 'Save All' button to save your configurations and send them to the always running Python script.

What it does:
* When located inside of the garage and the car's engine status is turned on, the garage will automatically open.
* Upon leaving the radius (radius is set to 100 meters), the garage will automatically close or ensure it is closed.
* Upon re-entering the radius, the garage will automatically know to open.

Also, the backend polls the car location and ignition status constantly. This is not the greatest solution, however it seems like the only way for this challenge. If Ford were
to implement a feature like this, there is no reason to constantly poll. And they could integrate it with either something like MyQ, or HomeLink. HomeLink is fairly expensive 
for auto manufacturers though, but MyQ integration would be considerably cheaper for car buyers.</br></br>
MyQ is just the beginning. This same concept can be introduced to a wide array of different IoT/Smart Home devices.
