from odoo import api, fields, models
import json
import requests
from odoo.exceptions import UserError, Warning

class account_asset_category(models.Model):
    _inherit='account.asset.category'
    x_type_id=fields.Char('x_type_id')

class ResPartnerCustomization(models.Model):
    _inherit = 'res.partner'
    x_company_id=fields.Char('x_company_id')
    x_mautic_id = fields.Char('ID')
    x_mautic_exported = fields.Boolean('x_is_exported', default=False)
    x_is_updated = fields.Boolean('x_is_updated', default=False)
    
    '''-----------Code for export_customer here-----------------------'''
    @api.model
    def export_customer(self):
#         print("export_customer is calling:::::::::::::",self)
        if len(self) > 1:
            raise UserError("Please Select one record at a time...!")
            return

        if self.x_mautic_id or self.x_mautic_exported:
            firstname=''
            lastname=''
            full_name_parent=''
            full_name=''
            if self.name : 
                    cust_name=self.name
                    if (' ' in cust_name):
                        print("if is printing------------------",self.name)
                        count_space=cust_name.count(' ')
                        if count_space==2:
                            full_name_parent=self.name.split(' ')
                            print("\n Full name as---------------",full_name_parent)
                            username = firstname + middlename + lastname
                        else:
                            full_name=self.name.split(' ')
                            print("\n Full name as---------------",full_name)
                            username = firstname +lastname
                
            company_obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
            if company_obj.mautic_access_token:
                url="https://mautic.pragtech.co.in/api/contacts/new"
#                 print("url::::::::::::::::::",url)   
                
                headers = {
                       'Authorization': 'Bearer {}'.format(company_obj.mautic_access_token),
                       'content-type':'application/json'
                       } 
                
                dict = {}
                if self.email:
                    dict['email'] = self.email
                if self.zip:
                    dict['zipcode'] = self.zip
                if (' ' in self.name):
                        if full_name_parent != '':
                            dict['firstname']=full_name_parent[0]
                        else:
                            dict['firstname']=full_name[0]
                else:
                    dict['firstname'] =self.name
                if (' ' in self.name):        
                    if full_name_parent != '':
                        dict['lastname'] = full_name_parent[2]
                    else:
                        dict['lastname']= full_name[1]
                if (' ' in self.name): 
                    if full_name_parent != '':
                        dict['middlename']=full_name_parent[1]
                if self.city:
                    dict['city'] = self.city
                if self.country_id:
                    dict['country'] = self.country_id.name
                
                if self.state_id:
                    dict['state'] = self.state_id.name
                if self.zip:
                    dict['zipcode'] = self.zip
                dict['isuser'] = True    
                payload = json.dumps(dict)
                print ("@@@@@@@@@@@@@@@@@@@@",payload)
                response = requests.post(url, data=payload,headers=headers)
                print ('response is ====', response.text)
                res = response.json()
                print(" customer is exported successsfully!!!!!!!!!!!!!!!!")
        else:
            if not self.parent_id:
                print ('the details are name as=================', self.name)
                firstname=''
                lastname=''
                middlename=''
                username = firstname +middlename+lastname
                full_name_parent=''
                full_name=''
                if self.name : 
                    cust_name=self.name
                    if (' ' in cust_name):
                        print("if is printing------------------",self.name)
                        count_space=cust_name.count(' ')
                        if count_space==2:
                            print("-------------first nane last neme--------",count_space)
                            full_name_parent=self.name.split(' ')
                            print("\n Full name as---------------",full_name_parent)
                            username = firstname + middlename + lastname
                        else:
                            full_name=self.name.split(' ')
                            print("\n Full name as---------------",full_name)
                            username = firstname +lastname
                
                company_obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
                if company_obj.mautic_access_token:
                    print ('access code is', company_obj.mautic_access_token)
                    url = "https://mautic.pragtech.co.in/api/contacts/new"
                    headers = {
                       'Authorization': 'Bearer {}'.format(company_obj.mautic_access_token),
                       'content-type':'application/json'
                       } 
                    dict = {}
                    if self.city:
                        dict['city'] = self.city
                    if self.phone:
                        dict['phone'] = self.phone
                    if (' ' in self.name):
                        if full_name_parent != '':
                            dict['firstname']=full_name_parent[0]
                        else:
                            dict['firstname']=full_name[0]
                    else:
                        dict['firstname'] =self.name
                    if (' ' in self.name): 
                        if full_name_parent != '':
                            dict['lastname'] = full_name_parent[2]
                        else:
                            dict['lastname']= full_name[1]
                    if (' ' in self.name): 
                        if full_name_parent != '':
                            dict['middlename']=full_name_parent[1]
                            print("-----------in the full_name_parent Middale name as-------",dict['middlename'])
                            
                    if self.email:
                        dict['email'] = self.email
                    else:
                        dict['email']= self.name+'@odoo.com'
                    if self.country_id:
                        dict['country'] = self.country_id.name
                    if self.street:
                        dict['address1'] = self.street 
                    if self.street2:
                        dict['address2'] = self.street2     
                    if self.zip:
                        dict['zipcode'] = self.zip
                        
                    print("\n \n Dict of customer as-------------------",dict)
                    dict['isuser'] = True
                    payload = json.dumps(dict)
                    print ("++++++++++",payload)
                    print ("In export",json.dumps(payload))
                    response = requests.post(url, data=payload,headers=headers)
                    print ('response is ====', response)
                    if response.text:
                        print("\n --------response is----------------",response.text)
                        res = response.json()
                        print("resssssssssssssssssssssssssssssssssssssss",res)
                        x_mautic_id = res.get('contact').get('id')
                        if x_mautic_id:
                            dict_write = {'x_mautic_id': str(x_mautic_id),
                                          'x_is_exported': True}
                            self.write(dict_write)
                        print(" customer is exported successsfully!!!!!!!!!!!!!!!!")
                        
    
    '''-------------------------code of export_company here-----------------------------'''                    
    @api.model
    def export_company(self):
        if len(self) > 1:
            raise UserError("Please Select one record at a time...!")
            return  
        
        if self.x_mautic_id or self.x_mautic_exported:
            print("RECORD IS ALREADY EXPORTED UPDATING THE RECORDS",self.x_mautic_id,self.x_mautic_exported)
            
        company_obj=self.env['res.company'].search([('id','=',self.company_id.id)])
#         print("\n\n\n==========compnay_obj===============",company_obj)
         
        if company_obj.mautic_access_token:
#             print("\n\n\n====company_obj.mautic_access_token==========",company_obj.mautic_access_token)
            url="https://mautic.pragtech.co.in/api/companies/new"
            headers={
                     'Authorization':'Bearer {}'.format(company_obj.mautic_access_token)
                     }
            data_dict={}
            
            if self.name:
                data_dict['companyname']=self.name
                
            if self.phone:
                data_dict['phone']=self.phone
                
            if self.mobile:
                data_dict['mobile']=self.mobile
                
            if self.email:
                data_dict['email']=self.email
                
            if self.website:
                data_dict['website']=self.website
                
            if self.street:
                data_dict['address1']=self.street
                
            if self.street2:
                data_dict['address2']=self.street2 
                
            if self.city:
                data_dict['city']=self.city 
                                
            if self.zip:
                data_dict['zipcode']=self.zip
                        
            if self.state_id:
                state_name=self.state_id.name
                state_id=self.env['res.country.state'].search([('name','=',self.state_id.name)])
                if state_id:
                    data_dict['state']=state_id.id
                    print("\n\n\n=====state=======",data_dict['state'])
                           
            if self.country_id:
                country_id=self.env['res.country'].search([('name','=',self.country_id.name)])
                if country_id:
                    data_dict['country']=self.country_id.name 
                    
            data_dict['isuser']=True  
            print("\n\n\n==========Dict of Export Company=====================>:",data_dict)
            
            payload = json.dumps(data_dict)
            print ("++++++++++",payload)
            print ("In export",json.dumps(payload))
            response = requests.post(url, data=payload,headers=headers)
            print ('response is ====', response,response.text)
            if response.text:
                res = response.json()
                print("\n \n res of company as-------------------------->",res)
                x_mautic_id = res.get('company').get('id')
                if x_mautic_id:
                    dict_write = {'x_mautic_id': str(x_mautic_id),
                                          'x_is_exported': True}
                    self.write(dict_write)
                    print(" company is exported successsfully!!!!!!!!!!!!!!!!")
