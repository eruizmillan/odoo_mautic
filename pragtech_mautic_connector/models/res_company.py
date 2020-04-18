import json
import logging
import requests
import codecs
import base64

from odoo import api, fields, models,exceptions ,_
from odoo.exceptions import ValidationError,UserError   
from urllib.parse import urlencode

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = "res.company"
    x_company_id=fields.Char('x_company_id')
    x_mautic_id = fields.Char('ID')
    x_mautic_exported = fields.Boolean('x_is_exported', default=False)
    x_is_updated = fields.Boolean('x_is_updated', default=False)
    #x_type_id=fields.Char('x_type_id')
    # company level mautic configuration field#
    mautic_client_id=fields.Char("Client ID")
    mautic_client_secret=fields.Char("Client Secret")
    mautic_auth_base_url=fields.Char('Authorization URL')
    
    mautic_request_token_url = fields.Char('Redirect URL', defualt="https://localhost:8011/get_auth_code ",   help="One of the redirect URIs listed for this project in the developer dashboard.")
    # used for api calling, generated during authorization process.
    mautic_auth_code=fields.Char('Auth Code')
    mautic_access_token=fields.Char('Access Token')
    
    @api.multi
    def authenticate(self):
        try:
            url = self.mautic_auth_base_url + '?client_id=' + self.mautic_client_id + '&redirect_uri=' + self.mautic_request_token_url + '&response_type=code&grant_type=authorization_code&code=UNIQUE_CODE_STRING'
            return {
                "type": "ir.actions.act_url",
                "url": url,
                "target": "new"
            }
        except Exception:
            raise ValidationError( _('Fill up the correct information...!!'))  
     
    @api.multi    
    def refresh_token(self):
        print("refresh_token is called successfully::::::::::::;;;;;",self)
        try:
            url = self.mautic_auth_base_url + '?client_id=' + self.mautic_client_id + '&redirect_uri=' + self.mautic_request_token_url + '&response_type=code&grant_type=refresh_token&code=UNIQUE_CODE_STRING'
            return {
                "type": "ir.actions.act_url",
                "url": url,
                "target": "new"
            }
        except Exception:
            raise ValidationError( _('Fill up the correct information...!!'))
    '''------------------Code Import Contact here----------------'''
    @api.multi   
    def  import_contacts(self):
        headers = {
                       'Authorization': 'Bearer {}'.format(self.mautic_access_token),
                       'content-type':'application/json'
                       }
        
        res= requests.get('https://mautic.pragtech.co.in/api/contacts?limit=6500',headers=headers)
        try:
            result = res.json()
            counter=0
            #result = res.json()
            for key, val in result.get('contacts').items():
                my_dict={}
                counter=counter+1
                
                res_partner = self.env['res.partner'].search([('x_mautic_id', '=', val.get("id"))]) 
                firstname=''
                lastname=''
                  
                if val.get('fields').get('core').get('firstname').get('value'):
                    firstname=val.get('fields').get('core').get('firstname').get('value')
                    
                if val.get('fields').get('core').get('lastname').get('value'):
                    lastname=val.get('fields').get('core').get('lastname').get('value')
                    
                if firstname or lastname:
                    
                    if val.get('id'):
                        my_dict['x_mautic_id']=val.get('id')
                           
                    if val.get('fields').get('core').get('address2').get('value'):
                        my_dict['street2'] =val.get('fields').get('core').get('address2').get('value')
                          
                    if val.get('fields').get('core').get('address1').get('value'):
                        my_dict['street']=val.get('fields').get('core').get('address1').get('value') 
                          
                    if val.get('mobile'):
                        my_dict['mobile'] =val.get('mobile')
                           
                    if val.get('fields').get('core').get('country').get('value'):
                        country_name=val.get('fields').get('core').get('country').get('value')
                        country_id=self.env['res.country'].search([('name','=',country_name)])
                        if country_id:
                            my_dict['country_id']=country_id.id
                        
                    if val.get('fields').get('core').get('email').get('value'):
                        my_dict['email']=val.get('fields').get('core').get('email').get('value')
                        
                    if val.get('fields').get('core').get('zipcode').get('value'):
                        my_dict['zip']=val.get('fields').get('core').get('zipcode').get('value')
                                
                    if firstname or lastname:
                        my_dict['name'] = firstname + ' ' + lastname
                        
                    if val.get('fields').get('core').get('state').get('value'):
                        state_name=val.get('fields').get('core').get('state').get('value')
                        state_id=self.env['res.country.state'].search([('name','=',state_name)])
                        if state_id:
                            my_dict['state_id']=state_id.id
                        
                    if val.get('fields').get('core').get('phone').get('value'):
                        my_dict['phone']=val.get('fields').get('core').get('phone').get('value')
                        
                    if  val.get('fields').get('core').get('city').get('value'):
                        my_dict['city']=val.get('fields').get('core').get('city').get('value')
                        
                    if val.get('fields').get('core').get('mobile').get('value'):
                        my_dict['mobile']=val.get('fields').get('core').get('mobile').get('value')
                    
                    if val.get('fields').get('core').get('website').get('value'):
                        my_dict['website']=val.get('fields').get('core').get('website').get('value')
                        
                    if val.get('fields').get('core').get('position').get('value'):
                        my_dict['function']=val.get('fields').get('core').get('position').get('value')
                     
                    if not res_partner:
                        child_create = self.env['res.partner'].create(my_dict)
                    else:
                        write_obj = res_partner.write(my_dict)
                           
                    print("RECORD EDITED SUCCESSFULLY",my_dict)    
                          
                else:
                    print("records doesn't content any name")  
         
        except Exception as e:
            raise Warning("null values") 
        
    '''-------------------Code for Import Asset here--------------------'''
    @api.multi
    def import_company(self):
        print("enter in to company",self)  
        headers = {
                       'Authorization': 'Bearer {}'.format(self.mautic_access_token),
                       'content-type':'application/json'
                       }    
        
        res= requests.get('https://mautic.pragtech.co.in/api/companies?limit=200',headers=headers) 
        try:
            parsed_json=res.json()
        
            for key, val in parsed_json.get('companies').items():
                parent_id=self.env['res.company'].search([('x_company_id','=',val.get('id'))]).id
                data_dict={}
                if val.get('id'):
                    data_dict['x_company_id']=val.get('id')
                           
                if val.get('fields').get('all').get('companywebsite'):
                    data_dict['website']=val.get('fields').get('all').get('companywebsite')
                
                if val.get('fields').get('all').get('companycountry'):
                    country_name=val.get('fields').get('all').get('companycountry')
                    country_id=self.env['res.company'].search([('name','=',country_name)])
                    if country_id:
                        data_dict['country_id']=country_id.id
                data_dict['is_company']=True        
                #data_dict['company_type']='Company'
                        
                if val.get('fields').get('all').get('companyzipcode'):
                    data_dict['zip']=val.get('fields').get('all').get('companyzipcode')
                if val.get('fields').get('all').get('companycity'):
                    data_dict['city']=val.get('fields').get('all').get('companycity')
                if val.get('fields').get('all').get('companystate'):
                    state_name=val.get('fields').get('all').get('companystate')
                    state_id=self.env['res.country.state'].search([('name','=',state_name)])
                    if state_id:
                        data_dict['state_id']=state_id.id
                        
                if val.get('fields').get('all').get('companyaddress1'):
                    data_dict['street']=val.get('fields').get('all').get('companyaddress1')
                            
                if val.get('fields').get('all').get('companyaddress2'):
                    data_dict['street2']=val.get('fields').get('all').get('companyaddress2')
                
                if val.get('fields').get('core').get('companyemail').get('value'):
                    data_dict['email']=val.get('fields').get('core').get('companyemail').get('value')
                 
                if val.get('fields').get('core').get('companyname').get('value'):
                    data_dict['name']=val.get('fields').get('core').get('companyname').get('value')
                print("\n\n\n===========data_dict import_company =============",data_dict)
                    
                if not  parent_id:
                    parent_id=self.env['res.company'].create(data_dict)
                    print("company IS CREATED\t",parent_id.id)
                else:
                    count=0
                    count=count+1
                    write_object=self.env['res.company'].write(data_dict)
                    print("RECODS IS UPDATING\t",write_object)
                    print("count===is==on ===write==========",count)
                
        except Exception as e:
            raise Warning("not getting value")
        
    '''-------------------Code for Import Asset here--------------------'''
    @api.multi
    def import_asset(self):
#         print("\n\n\n\n\n enter into aseet:;;;;;;;;;;;;;;;",self)  
        headers = {
                       'Authorization': 'Bearer {}'.format(self.mautic_access_token),
                       'content-type':'application/json'
                       }    
        res= requests.get('https://mautic.pragtech.co.in/api/assets',headers=headers)
        try:
            parsed_json=res.json()
        except :
            print('Decoding JSON has failed')
            
        for rec in parsed_json.get('assets'):
            print("\n\n\n  rec::::::::::::::::::::::",rec)
            x_asset_mautic_id=self.env['account.asset.asset'].search([('x_asset_mautic_id','=',rec.get('id'))]).id
            print("\n\n\n============x_asset_mautic_id====,rec.get('id')=======",x_asset_mautic_id)
            data_dict={}
            
            if rec.get('title'):
                data_dict['name']=rec.get('title')
                  
            if rec.get('id'):
                data_dict['x_asset_mautic_id']=rec.get('id')
                    
            data_dict['isPublished']=True
            if rec.get('publishUp'):
                data_dict['date']=rec.get('publishUp')
            if rec.get('category'):
                category_name=rec.get('category').get('title')
                category_id=self.env['account.asset.category'].search([('name','=',category_name)])
                if not category_id:
                    value_dict={}
                    type_id=self.env['account.asset.category'].search([('x_type_id','=',category_id.id)])
#                     print("Type id as--------------------->",type_id)
                    if parsed_json.get('assets'):
                        value_dict['name']=rec.get('title')
                        value_dict['company_id']=1
                        value_dict['account_asset_id']=2
                        value_dict['method_number']=5
                        value_dict['method_period']=12
                        value_dict['journal_id']=1
                        value_dict['account_depreciation_id']=1
                        value_dict['account_depreciation_expense_id']=1
                          
                        if type_id:
                            create_id=self.env['account.asset.category'].create(value_dict)
                            print("\n\n\n=======done Create records ============",create_id)
                        else:
                            write_obj=self.env['account.asset.category'].write(value_dict)
                            print("\n\n\n========Write records=====",write_obj) 
                if category_id:
                    data_dict['category_id']=category_id.id
                else:
                    value_dict={}
                    type_id=self.env['account.asset.category'].search([('x_type_id','=',category_id.id)])
                    if parsed_json.get('assets'):
                        value_dict['name']=rec.get('title')
                        
                        if rec.get('category').get('id'):
                            value_dict['x_type_id']=rec.get('category').get('id')
                            value_dict['company_id']=1
                            value_dict['account_asset_id']=2
                            value_dict['method_number']=5
                            value_dict['method_period']=12
                            value_dict['journal_id']=1
                            value_dict['account_depreciation_id']=1
                            value_dict['account_depreciation_expense_id']=1
                           
                        if not type_id:
                            create_id=self.env['account.asset.category'].create(value_dict)
                            print("\n\n\n=======done with this============",create_id)
                            data_dict['category_id']=create_id.id
                        else:
                            write_obj=self.env['account.asset.category'].write(value_dict)
                            print("\n\n\n=====Write Record succesfully======",write_obj)  
            data_dict['value']=0.0        
            print("\n\n\n========data_dict of import_asset==========>AS:::",data_dict)
            
            #if  rec.get('id'):
            if not x_asset_mautic_id:    
                create_child=self.env['account.asset.asset'].create(data_dict)
                print("\n\n\n==========create_child ASSET IS IMPORTED TO ODOO============",create_child)
            else:
                write_obj=self.env['account.asset.asset'].write(data_dict)
                print("\n\n\n======ASSET IS ALREADY THERE==========",write_obj)    
                  
class asset_asset(models.Model):
    _inherit='account.asset.asset'
    
    x_asset_mautic_id=fields.Char('ID')
    x_mautic_id=fields.Char('x_mautic_id')
    
class product_produtct(models.Model):
    _inherit='product.template'
    
    x_product_id=fields.Char('x_product_id')
    x_product_exported=fields.Boolean('x_product_exported')
    x_product_updated=fields.Boolean('x_product_updated')
    
    
    mautic_client_id=fields.Char("Client ID")
    mautic_client_secret=fields.Char("Client Secret")
    mautic_auth_base_url=fields.Char('Authorization URL')
    
    mautic_request_token_url = fields.Char('Redirect URL', defualt="https://localhost:8011/get_auth_code ",   help="One of the redirect URIs listed for this project in the developer dashboard.")
    # used for api calling, generated during authorization process.
    mautic_auth_code=fields.Char('Auth Code')
    mautic_access_token=fields.Char('Access Token')
    
    '''------------------------Code for Export Product here------------------------'''
    @api.multi
    def export_product(self):
        if len(self) > 1:
            raise UserError("Please Select one record at a time!!!!!!")
            return  
        
        if self.x_product_id or self.x_product_exported:
            print("RECORD IS ALREADY EXPORTED UPDATING THE RECORDS",self.x_product_id,self.x_product_exported)
            
        company_obj=self.env['res.company'].search([('id','=',self.company_id.id)])
         
        if company_obj.mautic_access_token:
            url="https://mautic.pragtech.co.in/api/assets/new"
            headers={
                     'Authorization':'Bearer {}'.format(company_obj.mautic_access_token)
                     }
            data_dict={}
            
            if self.name:
                data_dict['title']=self.name
                
            if self.type:
                data_dict['category']=self.type
                    
            data_dict['isPublished']=True
            data_dict['storageLocation']='local' 
            print("\n\n\n=========data_dict of export_product===========>AS:::",data_dict)  
            pdf = self.env.ref('product.report_product_label').render_qweb_pdf([self.id])
            pdf=str(pdf) #convert to string here
            
            mystr_encoded = base64.b64decode((pdf.encode('ascii')))
#             print("\n\n\n======mystr_encoded============",mystr_encoded)
            decode=mystr_encoded.decode("utf-8", "ignore")
            
            payload=json.dumps(data_dict)
            print("============payload___________-",payload)
#             data=json.load(payload)
            response = requests.post(url, data=payload,headers=headers)
            print ('response is ====--------------------------', response,response.text)
            if response.text:
                res = response.json()
#                 print("resssssssssssssssssssssssssssssssssssssss",res)
#                 x_product_id = res.get('contact').get('id')
#                 if x_product_id:
#                     dict_write = {'x_mautic_id': str(x_product_id),
#                                           'x_is_exported': True}
#                     self.write(dict_write)
#                     print(" customer is exported successsfully!!!!!!!!!!!!!!!!")

