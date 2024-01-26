import asyncio
import json
import platform
import os
import cv2, time

from dotenv import load_dotenv
load_dotenv()

from aiortc import RTCPeerConnection, RTCSessionDescription,RTCConfiguration,RTCIceServer, MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay
from av import VideoFrame

import requests
user_name = 'pi_video_server'
peer_connections = set()

# server_url = 'http://127.0.0.1:8080/'
server_url = os.getenv('SERVER_URL')

# Sedning offer to the signalling server

def send_offer(data):
    data = {'user_name':user_name,
            'offer':data}
    response = requests.post(url = f'{server_url}offer_data',params=data)
    print(response.json())
    
async def get_answer():
    try:
        while True:
            response = requests.get(url=f'{server_url}get_answer/{user_name}')
            data = response.json()
            if data['success'] == True:
                print('Reponse Received')
                return data['answer']
            else:
                print(data)
            await asyncio.sleep(1)
    except:
        print('Keyboard error')


# for configuration of multiple stun and turn server

ice_servers = [RTCIceServer(urls='stun:___________________'),
               RTCIceServer(urls='turn:___________________',
                            username='____________________',
                            credential="___________________"),
               RTCIceServer(urls="turn:____________________________" ,
                            username = "__________________________",
                            credential ="_________________________" ),
               RTCIceServer(urls= "turn:________________________",
                            username = "__________________________",
                            credential = "_________________________"),
               RTCIceServer(urls= 'turn:____________________________',
                            username = "__________________________",
                            credential = "_________________________"),]

config = RTCConfiguration(iceServers=ice_servers)

google_ice = [RTCIceServer(urls='stun:stun.l.google.com:19302')]

config2 = RTCConfiguration(google_ice)

webcam = None
relay = None


# Currently its making 60 fps video @ 720p
def create_local_video():
    global webcam, relay
    if relay is None:
        options = {'framerate':'60','video_size':'1280x720'}
        webcam = MediaPlayer('/dev/video0',options=options)
        relay = MediaRelay()
    return relay.subscribe(webcam.video)



async def offer():
    print('Starting RTC connection')
    
    peer_connection = RTCPeerConnection(configuration=config2)
    peer_connections.add(peer_connection)
    
    @peer_connection.on('connectionstatechange')
    async def connection_status():
        print('*'*20)
        print('Connection status is ',peer_connection.connectionState,peer_connections)
        print('*'*20)
        if peer_connection.connectionState == 'connected':
            response =  await requests.get(f'{server_url}remove_offer',params= {'user_name': user_name})
            print(response.json())
            
        if peer_connection.connectionState == 'failed':
            print('Conecction Failed')
            await peer_connection.close()

        if peer_connection.connectionState == 'closed':
            peer_connections.discard(peer_connection)
            
            
    
    # Checking ice connection state messages to debug 
    @peer_connection.on('iceconnectionstatechange')
    async def on_iceconnectionstate():
        print('*'*20)
        print('ICE CONNECTION status is ',peer_connection.iceConnectionState)
        print('*'*20)
    
    
    # Checking ice gathering state messages to debug 
    @peer_connection.on('icegatheringstatechange')
    async def on_icegatheringstatechange():
        print('*'*20)
        print('ICE GATHERTING CONNECTION status is ',peer_connection.iceGatheringState)
        print('*'*20)
    
    
    # implementation of datachannel if text transfer is needed
    @peer_connection.on('datachannel')
    async def datachannel_event(channel):
        
        print('data channel created > ',channel)
        
        @channel.on('open')
        async def on_open(message):
            print('Connection Opened ',message)
            
        @channel.on('message')
        async def on_message(message):
            print('Got mesage > ',message)
            
        @channel.on('close')
        def on_close(message):
            print("Connection Closed ",message)

    
    # take the local video and add it to the streaming track
    video = create_local_video()
    peer_connection.addTrack(video)
    offer_decription = await peer_connection.createOffer()
    await peer_connection.setLocalDescription(offer_decription)
    
    offer_data = {'sdp':peer_connection.localDescription.sdp,
                  'type':peer_connection.localDescription.type}
    # print(json.dumps(offer_data))
    print('\n'*2)
    send_offer(json.dumps(offer_data))
    
    answer = await get_answer()
    
    answer_data = json.loads(answer)
    answer_data = RTCSessionDescription(sdp= answer_data['sdp'],
                                        type= answer_data['type'])
    await peer_connection.setRemoteDescription(answer_data)
    
    

# after one successful connection it again creating offer to get another answer.
# Basically webRTC multistreaming
async def main():
    try:
        while True:
            # data = int(input('create another offer ? '))
            data =1 
            if data == 1:
                await asyncio.gather(offer()) 
    except KeyboardInterrupt:
        print(KeyboardInterrupt)
    
if __name__ == '__main__':
    asyncio.run(main())  
    