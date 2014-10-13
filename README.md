Gait-Analysis-using-RGB-data
============================
This is our project we completed over Gait Recognition in the month of May 2014.

This work is focused on identifying a person with the help of his walking style by only collecting the rgb data.
This helps us to perform Gait Recognition with help of simple cameras, web cams without aid of infrared sensors,etc. It is done in python using OpenCV. 
We also achieved a tremendous success in our results as the accuracy of result was much higher as compared to earlier works over it.

To work with theses codes, you need to make a folder naming Gait_data_latest which contains all the .dcl format files (i.e. raw structure video)
Next, run the extract_rgb_from_dcl.m giving the input file name and frame number=500, 0/1 for training or test case.
After that run training_call_function.py
At end perform test by running test_call_function.py
