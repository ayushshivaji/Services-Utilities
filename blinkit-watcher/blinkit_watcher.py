import requests
import time
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import urllib.parse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Load environment variables
load_dotenv()

class BlinkitWatcher:
    def __init__(self, product_url, pincode, notification_service_url=None, check_interval=600):
        """
        Initialize the Blinkit watcher
        
        Args:
            product_url (str): URL of the Blinkit product to monitor
            pincode (str): Pincode to check availability for
            notification_service_url (str): URL of the notification service
            check_interval (int): Time between checks in seconds
        """
        self.base_url = product_url
        self.pincode = pincode
        self.product_url = self._add_pincode_to_url(product_url, pincode)
        self.notification_service_url = notification_service_url or os.getenv('NOTIFICATION_SERVICE_URL', 'http://localhost:10000/publish')
        self.check_interval = int(os.getenv('CHECK_INTERVAL', check_interval))
        self.last_check = None
        self.is_available = False
        
        # Enhanced headers to better mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'DNT': '1',
            'Referer': 'https://blinkit.com/',
            'Origin': 'https://blinkit.com'
        }
        
        # Create a session to maintain cookies
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _add_pincode_to_url(self, url, pincode):
        """Add pincode parameter to the URL"""
        # First visit the homepage to get necessary cookies
        try:
            self.session.get('https://blinkit.com/')
        except Exception as e:
            logging.error(f"Error visiting homepage: {e}")
        
        # Update the URL format to match current Blinkit structure
        # Remove /prn/ and /prid/ from the URL
        url = url.replace('/prn/', '/').replace('/prid/', '/')
        
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        query_params['pincode'] = [pincode]
        
        # Reconstruct the URL with the new query parameters
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        return urllib.parse.urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))

    def check_availability(self):
        """
        Check if the product is available on Blinkit for the specified pincode
        Returns True if available, False otherwise
        """
        try:
            logging.info(f"Checking availability for pincode {self.pincode}")
            response = self.session.get(self.product_url)
            
            # Save response to file
            filename = f"blinkit_response.html"
            filepath = os.path.join(LOGS_DIR, filename)
            
            # Get the response content, handling compression
            try:
                content = response.content.decode('utf-8')
            except UnicodeDecodeError:
                # If direct decode fails, try to handle gzip compression
                import gzip
                from io import BytesIO
                try:
                    content = gzip.decompress(response.content).decode('utf-8')
                except Exception as e:
                    logging.error(f"Failed to decode response: {e}")
                    content = f"Raw response (failed to decode): {response.content}"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Status Code: {response.status_code}\n")
                f.write(f"Headers: {json.dumps(dict(response.headers), indent=2)}\n")
                f.write("\nResponse Content:\n")
                f.write(content)
            
            logging.info(f"Saved response to {filepath}")
            
            if response.status_code == 404:
                logging.error(f"Product not found (404). The URL might be invalid or the product might have been removed.")
                logging.error(f"Current URL: {self.product_url}")
                return False
                
            if response.status_code == 403:
                logging.error("Access forbidden (403). Blinkit might be blocking automated requests.")
                logging.error("Try visiting the URL manually in a browser to verify the product exists.")
                return False
                
            if response.status_code == 200:
                page_content = content.lower()
                
                # Check for out of stock indicators
                out_of_stock_indicators = [
                    "out of stock",
                    "currently unavailable",
                    "sold out",
                    "not available",
                    "unavailable",
                    "not available in your area",
                    "delivery not available"
                ]
                
                # Check for add to cart button or similar elements
                add_to_cart_indicators = [
                    "add to cart",
                    "add to basket",
                    "buy now",
                    "order now",
                    "Add"
                ]
                
                # Check if any out of stock indicators are present
                for indicator in out_of_stock_indicators:
                    if indicator in page_content:
                        logging.info(f"Product is not available - found indicator: {indicator}")
                        return False
                
                # Check if any add to cart indicators are present
                for indicator in add_to_cart_indicators:
                    if indicator in page_content:
                        logging.info(f"Product is available - found indicator: {indicator}")
                        return True
                
                logging.info("Product is not available - no availability indicators found")
                return False
                
            logging.warning(f"Received non-200 status code: {response.status_code}")
            return False
        except Exception as e:
            logging.error(f"Error checking availability: {e}")
            return False

    def notify(self):
        """Send notification through the local notification service"""
        try:
            # Prepare the message
            message = f"🎉 Hocco Aamchi Mango Ice Cream is now available!\n" \
                     f"📍 Pincode: {self.pincode}\n" \
                     f"🔗 {self.product_url}\n" \
                     f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Prepare the payload
            payload = {
                "message": message
            }

            # Make the API call
            response = requests.post(
                self.notification_service_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("Successfully sent notification")
            else:
                print(f"Notification failed with status code: {response.status_code}")
                print(f"Response: {response.text}")

        except Exception as e:
            print(f"Error sending notification: {e}")

    def watch(self):
        """Start watching for product availability"""
        print(f"Starting to watch Hocco Aamchi Mango Ice Cream on Blinkit")
        print(f"Pincode: {self.pincode}")
        print(f"Checking every {self.check_interval} seconds")
        print(f"Notification Service: {self.notification_service_url}")
        
        while True:
            current_time = datetime.now()
            if self.last_check:
                time_since_last_check = (current_time - self.last_check).total_seconds()
                if time_since_last_check < self.check_interval:
                    time.sleep(1)
                    continue

            self.last_check = current_time
            is_available = self.check_availability()
            
            if is_available and not self.is_available:
                print(f"\nProduct is now available! ({current_time})")
                self.notify()
            elif not is_available and self.is_available:
                print(f"\nProduct is no longer available ({current_time})")
            
            self.is_available = is_available
            print(f"Last check: {current_time.strftime('%H:%M:%S')} - Available: {is_available}", end='\r')

def main():
    # Blinkit product URL
    product_url = os.getenv('PRODUCT_URL', "https://blinkit.com/prn/hocco-aamchi-mango-ice-cream-cup/prid/657166")
    
    # Get pincode from environment variable or use default
    pincode = os.getenv('PINCODE', '201017')
    while not pincode.isdigit() or len(pincode) != 6:
        print("Invalid pincode. Please enter a valid 6-digit pincode.")
        pincode = input("Enter your pincode: ").strip()
    
    # Create and start watcher
    watcher = BlinkitWatcher(product_url, pincode)
    watcher.watch()

if __name__ == "__main__":
    main() 