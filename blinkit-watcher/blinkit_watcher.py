import requests
import time
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import urllib.parse

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
        
        # Headers to mimic a browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

    def _add_pincode_to_url(self, url, pincode):
        """Add pincode parameter to the URL"""
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
            response = requests.get(self.product_url, headers=self.headers)
            
            if response.status_code == 200:
                page_content = response.text.lower()
                
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
                    "order now"
                ]
                
                # Check if any out of stock indicators are present
                for indicator in out_of_stock_indicators:
                    if indicator in page_content:
                        return False
                
                # Check if any add to cart indicators are present
                for indicator in add_to_cart_indicators:
                    if indicator in page_content:
                        return True
                
                return False
                
            return False
        except Exception as e:
            print(f"Error checking availability: {e}")
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
    product_url = "https://blinkit.com/prn/hocco-aamchi-mango-ice-cream-cup/prid/657166"
    
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