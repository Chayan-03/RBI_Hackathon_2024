import requests
import base64
import time
import ssl
import socket
import OpenSSL.crypto as crypto

VT_API_KEY = 'YOUR_VIRUSTOTAL_API_KEY'
GEO_API_KEY = 'YOUR_GEOLOCATION_API_KEY'

def scan_url(url):
    headers = {
        "x-apikey": VT_API_KEY
    }
    data = {
        'url': url
    }
    response = requests.post('https://www.virustotal.com/api/v3/urls', headers=headers, data=data)
    return response.json()

def get_url_report(url):
    headers = {
        "x-apikey": VT_API_KEY
    }
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip('=')
    response = requests.get(f'https://www.virustotal.com/api/v3/urls/{url_id}', headers=headers)
    return response.json()

def get_server_location(ip):
    response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={GEO_API_KEY}&ip={ip}')
    return response.json()

def get_ssl_certificate(url):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=url) as sock:
            sock.settimeout(10)
            sock.connect((url, 443))
            cert_data = sock.getpeercert(True)
            cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data)
            
            subject = cert.get_subject()
            issuer = cert.get_issuer()
            cert_type = cert.get_signature_algorithm().decode()
            
            return {
                "subject": dict(subject.get_components()),
                "issuer": dict(issuer.get_components()),
                "cert_type": cert_type
            }
    except Exception as e:
        print(f"Error retrieving SSL certificate: {e}")
        return None

def check_url_safety(url):
    scan_result = scan_url(url)
    time.sleep(10)
    report = get_url_report(url)
    is_malicious = report['data']['attributes']['last_analysis_stats']['malicious'] > 0
    
    ip = report['data']['attributes'].get('last_http_response', {}).get('ip_address', None)
    server_location = get_server_location(ip) if ip else 'IP address not available'
    
    related_entities = report['data'].get('relationships', {}).get('undetected_urls', {}).get('data', [])
    related_to_cybercrime = any(entity['attributes']['last_analysis_stats']['malicious'] > 0 for entity in related_entities)
    
    redirects = report['data']['attributes'].get('last_http_response', {}).get('redirects_to', None)
    redirects_to_fraud = False
    if redirects:
        redirect_report = get_url_report(redirects)
        redirects_to_fraud = redirect_report['data']['attributes']['last_analysis_stats']['malicious'] > 0
    
    related_to_financial_fraud = False
    if 'categories' in report['data']['attributes']:
        categories = report['data']['attributes']['categories']
        if 'online_banking' in categories or 'financial_services' in categories:
            related_to_financial_fraud = True
    
    redirects_to_financial_fraud = False
    if redirects:
        redirect_categories = redirect_report['data']['attributes'].get('categories', [])
        if 'online_banking' in redirect_categories or 'financial_services' in redirect_categories:
            redirects_to_financial_fraud = True
    
    website_type = report['data']['attributes'].get('type_description', 'Type not available')
    
    ssl_certificate = get_ssl_certificate(url)
    
    has_certificate = ssl_certificate is not None
    
    total_risk_factors = 7
    risk_factors = sum([is_malicious, related_to_cybercrime, redirects_to_fraud, redirects_to_financial_fraud, related_to_financial_fraud, has_certificate])
    risk_percentage = (risk_factors / total_risk_factors) * 100
    
    return {
        "is_malicious": is_malicious,
        "server_location": server_location,
        "related_to_cybercrime": related_to_cybercrime,
        "redirects_to_fraud": redirects_to_fraud,
        "related_to_financial_fraud": related_to_financial_fraud,
        "redirects_to_financial_fraud": redirects_to_financial_fraud,
        "website_type": website_type,
        "has_certificate": has_certificate,
        "ssl_certificate_details": ssl_certificate,
        "risk_percentage": risk_percentage
    }

# Example usage
if __name__ == "__main__":
    test_url = 'http://testsafebrowsing.appspot.com/s/malware.html'
    result = check_url_safety(test_url)
    print(result)
