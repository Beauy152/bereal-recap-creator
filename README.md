# bereal-recap-creator
 A cli app to generate a recap video for bereal.

Simply login & memories will be automatically downloaded, resized & compiled into a shareable video.
 

This is by no means optimised nor particularly efficient - but it works!

## Pre-requisites

### BeReal API
In order to access the bereal api's required, you can use the following [repository](https://github.com/chemokita13/beReal-api) by [@chemokita13](https://github.com/chemokita13). simply follow the steps in the repository readme to start the api locally.

### Python libraries

the program was developed using `python3.11`, and all required libraries are located in `requirements.txt`.

## Usage

Upon running the application, the program will connect to the api & allow the user to login via OTP; The program will then download the relevant memories from & create the recap video.


 ```bash
 python main.py -p <phone-number> -y <year> [-u <bereal-api-url>] [-f <desired-fps>]
 ```


### Note -

This is in no way affiliated with BeReal.
