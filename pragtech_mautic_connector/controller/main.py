from odoo import http
from odoo.http import request
import requests
import base64
import json
from urllib.parse import urlencode



class Custom_mautic_controller(http.Controller):
   
    @http.route('/get_auth_code', type="http", auth="public", website=True)
    def get_auth_code(self, **kwarg):
        data = None
        comp = http.request.env['res.users'].sudo().search([], limit=1).company_id
        if kwarg.get('code'):
            code = kwarg.get('code')
            url = urlencode({'redirect_uri':comp.mautic_request_token_url})
            print ("Encoded URL ",url)
            data = "client_id={}&client_secret={}&{}&code={}&grant_type={}".format(comp.mautic_client_id,
                                                                                  comp.mautic_client_secret,
                                                                                  url,
                                                                                  code,
                                                                                  'authorization_code')
            print ("DATA IS ",data)
          
            headers = {
                       'content-type' : 'application/x-www-form-urlencoded'
                       }
               
   
            res = requests.request('POST','https://mautic.pragtech.co.in/oauth/v2/token',headers=headers,
                                    data = data)
            print (res.text)
            parsed_response = json.loads(res.text)
            print("parsed_response::::::::::::::::",parsed_response)
            print ('\n\Token is  is ===\n', parsed_response.get('access_token'))
            comp.write({'mautic_access_token': parsed_response.get('access_token')})
            print("\n\n\mautic_access_token",parsed_response.get('access_token'))
            comp.write({'mautic_client_id': comp.mautic_client_id})
            comp.write({'mautic_auth_code': code})
            print("n\n\n\n mautic_client_id",comp.mautic_client_id)
            comp.write({'mautic_client_secret': comp.mautic_client_secret})
            print("\n\n\n\n\n mautic_client_secret",comp.mautic_client_secret)
            comp.write({'redirect_uri':comp.mautic_request_token_url})
            print("\n\n\n\n\n\n\n redirect_uri",comp.mautic_request_token_url)
            return "Successfully Connected,Please Close this window"
         
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#         print "\nInside Custom get_auth_code", kwarg
#         if kwarg.get('code'):
#             print '\n\nthe code is =====\t', kwarg.get('code')
#             code = kwarg.get('code')
#             print 'type is ', type(code)
# 
#             headers = {'Api-Version': 'alpha', 'Content-Type': 'application/json'}
#             payload = {'grant_type': 'authorization_code',
#                        'client_secret': '08e2647b3ac3bb7f4a878fe02db8c8325b4da8fec315724690d4a814796fb46d',
#                        
#                        'code': code,
#                        'client_id': 'c277353aa6e015ba2df5c28228e070fd25159b88a11c2abf43ff25dbec641778',
#                        'redirect_uri': 'https://239699cc.ngrok.io/get_auth_code'
#             }    
# 
# 
#             print 'payload is =====', payload
# 
#             res = requests.post('https://api.freshbooks.com/auth/oauth/token',
#                                 data=json.dumps(payload),
#                                 headers=headers)
#             salesforce_id = http.request.env['res.users'].sudo().search([], limit=1).company_id
#             salesforce_id.write({'fb_auth_code': kwarg.get('code')})
#             parsed_response = json.loads(res.text)
#             print '\n\Token is  is ===\n', parsed_response.get('access_token')
#             salesforce_id.write({'fb_access_token': parsed_response.get('access_token')})
#             salesforce_id.write({'fb_client_id': 'a7b9b091fd7c6a48b62d43bc132d94dcf936d189397006c331e4d4f4f7f924a9'})
#             salesforce_id.write({'fb_client_secret': '08e2647b3ac3bb7f4a878fe02db8c8325b4da8fec315724690d4a814796fb46d'})
#             salesforce_id.write({'redirect_uri':'https://7ff03f6c.ngrok.io/get_auth_code'})
#     #         if kwarg.get('code'):
#     #             print '\n\ncode is\t',kwarg.get('code')
#     #             '''Get access Token and store in object'''
#     #             salesforce_id = http.request.env['res.users'].sudo().search([],limit=1).company_id
#     #             print '\n\nsales force id is==== ', salesforce_id.id
#     #             if salesforce_id:
#     #                 print '\n\nsales force id is==== ', salesforce_id.id
#     #
#     #                 salesforce_id.write({'fb_auth_code':kwarg.get('code')})
#     #                 code =  kwarg.get('code')
#     #                 client_id = salesforce_id.fb_client_id
#     #                 client_secret = salesforce_id.fb_client_secret
#     #                 redirect_uri = salesforce_id.fb_request_token_url
#     #                 access_url = salesforce_id.fb_access_token_url
#     #
#     #
#     #                 headers = {'Api-Version': 'alpha', 'Content-Type': 'application/json'}
#     #                 payload = {'grant_type': 'authorization_code',
#     #                             'client_secret':client_secret,
#     #                            'code':code,
#     #                            'client_id':client_id,
#     #                            'redirect_uri':redirect_uri}
#     #
#     #
#     #                 access_token = requests.post(access_url,data=payload,headers=headers)
#     #                 print 'access_token is :\n', access_token
#     #                 if access_token:
#     #                     print "GOT ACCESS TOKEN",access_token.text
#     #                     parsed_token_response = json.loads(access_token.text)
#     #                     if parsed_token_response:
#     #                         salesforce_id.write({'fb_access_token':parsed_token_response.get('access_token')})
#     #                         print "Access token was set"
#         return "DONE"

