import cv2
import os
import re
import requests
import base64
import time
import ssl
import socket
import OpenSSL.crypto as crypto
from tabulate import tabulate

# Define the VirusTotal API key
VT_API_KEY = 'd5458d3b59c3d7378e05cbeb994d77eaf953b565b272106739d61a8578365992'

# Function to extract URLs from a text
def extract_urls(text):
    url_pattern = re.compile(
        r'(?:(?:https?|ftp):\/\/)?(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+[^ ]*'
    )
    urls = re.findall(url_pattern, text)
    urls_string = ' '.join(urls)
    return urls_string

# Function to check if a URL exists
def check_url_exists(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad responses
        return True
    except requests.RequestException as e:
        return f"URL '{url}' does not exist: {str(e)}"

# Function to scan a URL using VirusTotal
def scan_url(url):
    headers = {
        "x-apikey": VT_API_KEY
    }
    data = {
        'url': url
    }
    response = requests.post('https://www.virustotal.com/api/v3/urls', headers=headers, data=data)
    return response.json()

# Function to get URL report from VirusTotal
def get_url_report(url):
    headers = {
        "x-apikey": VT_API_KEY
    }
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip('=')
    response = requests.get(f'https://www.virustotal.com/api/v3/urls/{url_id}', headers=headers)
    return response.json()

# Function to get SSL certificate details of a URL
def get_ssl_certificate(url):
    if ".onion" in url:
        return None
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
    except Exception:
        return None

# Function to calculate risk percentage
def calculate_risk_percentage(scores, weights):
    total_weight = sum(weights)
    if total_weight == 0:
        return 0
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    risk_percentage = (weighted_sum / (total_weight * 100)) * 100
    return risk_percentage

# Function to check URL safety
def check_url_safety(url):
    if not check_url_exists(url):
        return {"url": url, "error": "URL does not exist"}
    
    scan_result = scan_url(url)
    time.sleep(10)
    report = get_url_report(url)
    
    if 'data' not in report or 'attributes' not in report['data']:
        return {"url": url, "error": "URL report not available"}
    
    attributes = report['data']['attributes']
    is_malicious = attributes.get('last_analysis_stats', {}).get('malicious', 0) > 0
    
    if is_malicious:
        return {
            "url": url,
            "is_malicious": True,
            "related_to_cybercrime": None,
            "redirects_to_fraud": None,
            "has_certificate": None,
            "ssl_certificate_details": None,
            "risk_percentage": 100,
            "confidence": "High risk - Avoid clicking"
        }
    
    related_entities = report['data'].get('relationships', {}).get('undetected_urls', {}).get('data', [])
    related_to_cybercrime = any(entity['attributes']['last_analysis_stats']['malicious'] > 0 for entity in related_entities)
    redirects = attributes.get('last_http_response', {}).get('redirects_to', None)
    redirects_to_fraud = False
    if redirects:
        redirect_report = get_url_report(redirects)
        redirects_to_fraud = redirect_report['data']['attributes']['last_analysis_stats']['malicious'] > 0
    
    ssl_certificate = get_ssl_certificate(url)
    has_certificate = ssl_certificate is not None
    
    score_malicious_flag = 100 if is_malicious else 0
    score_ssl_certificate = 100 if has_certificate else 0
    score_cybercrime_association = 100 if related_to_cybercrime else 0
    score_redirects_to_fraud = 100 if redirects_to_fraud else 0
    
    weights = {
        "malicious_flag": 3,
        "ssl_certificate": 1,
        "cybercrime_association": 2,
        "redirects_to_fraud": 2
    }
    
    risk_percentage = calculate_risk_percentage([score_malicious_flag, score_ssl_certificate, 
                                                 score_cybercrime_association, score_redirects_to_fraud],
                                                weights.values())
    
    if risk_percentage <= 25:
        confidence = "Low risk - Safe to click"
    elif risk_percentage <= 50:
        confidence = "Medium risk - Exercise caution"
    else:
        confidence = "High risk - Avoid clicking"
    
    result = {
        "url": url,
        "is_malicious": is_malicious,
        "related_to_cybercrime": related_to_cybercrime,
        "redirects_to_fraud": redirects_to_fraud,
        "has_certificate": has_certificate,
        "ssl_certificate_details": ssl_certificate,
        "risk_percentage": risk_percentage,
        "confidence": confidence
    }
    
    return result

# Main function to integrate QR code detection and URL safety check
def main():
    # Define the image path
    image_path = 'Untitled.png'

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    # Load the image
    image = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if image is None:
        print("Error: Image not loaded properly.")
        return

    # Initialize the QR code detector
    qrCodeDetector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)

    if points is not None:
        points = points[0]  # Extract the points array from the nested array
        nrOfPoints = len(points)
        # Draw lines around the QR code
        for i in range(nrOfPoints):
            nextPointIndex = (i + 1) % nrOfPoints
            pt1 = (int(points[i][0]), int(points[i][1]))
            pt2 = (int(points[nextPointIndex][0]), int(points[nextPointIndex][1]))
            cv2.line(image, pt1, pt2, (255, 0, 0), 5)

        print("Decoded Text from QR Code:", decodedText)

        # Extract URLs from the decoded text
        extracted_urls = extract_urls(decodedText)
        print("Extracted URLs:", extracted_urls)

        table = []
        for url in extracted_urls.split():
            result = check_url_safety(url)
            row = [
                result.get("url"),
                result.get("is_malicious"),
                result.get("related_to_cybercrime"),
                result.get("redirects_to_fraud"),
                result.get("confidence")
            ]
            table.append(row)

        # Print results in a tabular format
        headers = ["URL", "Malicious", "Related to Cybercrime", "Redirects to Fraud", "Confidence"]
        print(tabulate(table, headers=headers))

        # Display the image with detected QR code
        # cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("QR code not detected")

if __name__ == "__main__":
    main()
