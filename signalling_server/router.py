from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import os



app = FastAPI()
folder_path = os.path.abspath(os.path.dirname(__file__))
templates = Jinja2Templates(f'{folder_path}/templates')

testing_dict = {'Call' : {'url':'call_page'},
                'answer' : {'url': 'answer_page'},
                'live_feed_server': {'url': 'live_feed_server'}}

# storing the offers as dict
offers = {}

@app.get('/')
def home(request : Request):
    # print(request.url)
    return templates.TemplateResponse('home.html',{"request" : request, 'data': testing_dict })

# this page is for text communication
@app.get('/call_page')
def call_page(request: Request):
    # return {'Message' : f'you have came to URL page {request.url}'}
    return templates.TemplateResponse('call_page.html',{'request':request, 
                                                        "offer_url" : "saving_offers"})

@app.post('/offer_data')
def saving_offers(request: Request,user_name, offer):
    print(user_name)
    print(offer)
    print(type(offer))
    offers[user_name] = {'offer': offer}
    return {'success' : True}

# it takes answer from the answerer
@app.post('/answer_data')
def answer_data(user_name, answer):
    
    offers[user_name]['answer'] = answer
    return {'success': True}


# after the answer is store it returns them
@app.get('/get_answer/{user_name}')
def get_answer(user_name):
    if user_name not in offers:
        
        return {'success' : False,
                'error' : "username not found"}
    elif 'answer' in offers[user_name]:
        
            return {'success': True,
                    'user_name':user_name,
                    'answer':offers[user_name]['answer']}
    else:
        return {'success' : False,
                'error' : "not answered yet"}


# return the available offers stored in dict
@app.get('/get_offers')
def get_offers():
    return offers

# get offer for that username
@app.get('/get_offers/{user_name}')
def get_offers(user_name,request: Request):
    print(user_name)
    # return {'Message' : f'you have came to URL page {request.url}'}
    if user_name not in offers:
        
        return {'success' : False,
                'error' : "username not found"}
    elif 'offer' in offers[user_name]:
        
            return {'success': True,
                    'user_name':user_name,
                    'offer':offers[user_name]['offer']}
    else:
        return {'success' : False,
                'error' : "no offer yet"}
    
    
# it stores the offer. 
# Created for -
# if answer is given then for new offer    
@app.get('/remove_offer')
def remove_offer(user_name,request: Request):
    global offers
    # print(offers)
    if user_name not in offers:
        return {'success' : False,
                'error': 'Key not found'}
    else:
        offers.pop(user_name)
        print(f'{user_name} deleted {request.client}')
        return {'success' : True,
                'message' : 'deleted offer'}


# return web page for answering
@app.get('/answer_page')
def answer_page(request: Request):
    options = offers.keys()
    # return {'Message' : f'you have came to URL page {request.url}'}
    return templates.TemplateResponse('answer_page.html',{'request': request,
                                                          'options' : options})
    

# return a webpage for live feed camera
@app.get('/live_feed_server')
def live_feed_server(request : Request):
    options = offers.keys()
    
    return templates.TemplateResponse('live_feed_answer.html',{'request': request,
                                                               'options': options})





if __name__ == '__main__':
    uvicorn.run('router:app', host='0.0.0.0', port= 8080,reload= True, workers= 2)