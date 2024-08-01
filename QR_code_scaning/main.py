from qr_decoder.py import decode_qr_code
from url_scanner import check_url_safety
#from database_check import check_database
image_path = 'Untitled.png'
def main(image_path):
    decoded_info = decode_qr_code(image_path)
    
    if not decoded_info:
        print("No QR code detected")
        return
    
    if decoded_info.startswith("http://") or decoded_info.startswith("https://"):
        url_result = check_url_safety(decoded_info)
        print("URL Scan Result:", url_result)
    #else:
        #if check_database(decoded_info):
            #print("Information found in the database")
        #else:
            #print("Information not found in the database")

# Example usage
if __name__ == "__main__":
    main('path_to_qr_code_image.png')
