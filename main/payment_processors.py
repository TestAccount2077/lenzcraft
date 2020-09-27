from abc import ABC, abstractmethod

import requests
import hashlib
from secrets import token_urlsafe as token


class PaymentProcessor(ABC):
    
    @staticmethod
    def build(type, *args, **kwargs):
        
        types_and_processors = {
            'tracknpay': TrackNPayProcessor
        }
        
        return types_and_processors[type](*args, **kwargs)
        
    @abstractmethod
    def process_one_time_payment(self, data):
        
        pass
        
        
class TrackNPayProcessor(PaymentProcessor):
    
    API_KEY = "ab62ff8e-f03b-4421-b836-b654df23d99df"
    SALT = "0we6063d41058689513fa536be8db95637a6c15ed"
    REQUEST_URL = "https://biz.traknpay.in/v2/paymentrequest"
    
    def process_one_time_payment(self, data):
        
        try:
            
            request_data = dict(
                api_key=self.API_KEY,
                order_id=self._generate_order_id(),
                return_url='http:localhost:8002/payment-response/',
                hash=self._get_hash(data.request_data),
                mode='TEST',
                **data.request_data
            )
            
            response = requests.post(self.REQUEST_URL, request_data)
            
            response.raise_for_status()
            
            response_data = response.text
            
            print(response_data)
            
            return response_data, True
            
        except Exception as e:
            print(e)
            return {'error': 'Something went wrong when processing your payment.'}, False
            
    def _generate_order_id(self):
        
        return token()
        
    def _get_hash(self, request_data):
        
        sequence = "address_line_1|address_line_2|amount|api_key|city|country|currency|description|email|mode|name|order_id|phone|return_url|state|udf1|udf2|udf3|udf4|udf5|zip_code"
    	
        hash_string = self.SALT
        hashVarsSeq = sequence.split('|')
    	
        for i in hashVarsSeq:
        	if i in request_data.keys():
        		if len(str(request_data[i])) > 0:
        			hash_string += '|'
        			hash_string += str(request_data[i])
                    
        hash = hashlib.sha512(hash_string.encode()).hexdigest().upper()
        
        return hash
