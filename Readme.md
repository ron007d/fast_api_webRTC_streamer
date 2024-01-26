![](./banner%20for%20github%20webrtc%20streamer.png)
# FAST API FOR WEBRTC
A FAST API SINGALLING SERVER WITH AIORTC WEB STREAMER

## Setup
1. For signalling server install the `signalling_server_req.txt` using pip
```bash
pip3 install -r signalling_server_req.txt
```
2. For camera_streamer install the `camera_stream_req.txt` using pip
```bash
pip3 install -r signalling_server_req.txt
```
3. Change the server address for [webcam_streamer.py](./camera_code/webcam_streamer.py#L19)
    
    a. Change the code  - Hard code the address in the py file as server_url
    b. create .env file in the `camera_code` directory
```env
HOST=xxx.xxx.xxx.xxx
PORT=xxxx
SERVER_URL=http://${HOST}:${PORT}/
```



## How to run

1. run router.py from signalling_server folder
```bash
python3 signalling_server/router.py
```
2. in another system from where you want to stream video output run the camera_code
```bash
python3 camera_code/webcam_streamer.py
```
The implementation flows and learning flow works like this.
---
## Implementation flow
1. FAST API will work as a signalling server.
2. Currently it will follow only request response model but in later time websocket or socket io will be implemented.
3. There will be two user call and answer.
    
    a. Call will create username/room
    
    b. answer will check all the username/room list and select one and will try to connect to that.

---
## Supporting features
1. Added support python aiortc.
2. video quality needed to be fixed on aiortc side.



## workdone
| Index | Work | Under Planning | Under Progress | Testing | Completeds | Comments |
|:--:|:---|:---:|:--:|:---:|:---:|:--|
|1|Create a simple page with two redirects call and answer | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | |
|2| In the call page create a SDP (Session description) and send it to the fast api | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Sending to `localhost:8080/offer_data` as post request |
|3| Add Java script to get the answer response from another points | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Added java script which request from `localhost:8080/get_answer/<username>` if anyone answers from answer page then it will take it and connect with the client |
|4| create answer page where the offers will be shown and user can select those | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | took the keys from the `offers` directionay and passed it to jinja compiler |
|5| Get the offer from the selected user and create `answer SDP`  and pass it to the  `answer_data`| :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Done |
|6| Check the whole flow and test if it working |:white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | text is being transmitted and ICE candidate is working :blush:
|7| Create a simple HTML page and transmit video using WEB RTC | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Created using miniwebrtc github and working |
|8| Test the video transmission in LAN | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | LAN CONNECTION WORKING WITH VIDEO TRANSMISSION |
|9| Test the video in NAT transmission | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Done |
|10| Python AIORTC code to stream video from camera | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Done  |
|10| Python AIORTC code to Get video stream from another source | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | you can add other sources of the video also like video or a camera which is currently in your resident and streaming RTSP stream |


### Issues

1. only `Text mode is working in LAN and WAN` where the ice candiadates are getting success but in `video mode only LAN` ice candidate is working. 

    > Issue resolved by adding turn :white_check_mark:

2. Added turn server but still its not working properly.
    > Needed more testing to confirm the issue. :white_check_mark:


## Inspried by
https://github.com/xem/miniWebRTC
