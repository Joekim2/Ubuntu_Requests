
import os
import requests
from urllib.parse import urlparse, unquote
import time
from pathlib import Path


def create_fetched_images_directory():
    """
    Create the Fetched_Images directory if it doesn't exist.
    Ubuntu principle: Sharing - Organize content for later sharing
    """
    directory = "Fetched_Images"
    os.makedirs(directory, exist_ok=True)
    print(f"✓ Directory '{directory}' is ready for use")
    return directory


def extract_filename_from_url(url):
    """
    Extract filename from URL or generate one if not available.
    Ubuntu principle: Practicality - Handle various URL formats gracefully
    """
    try:
        # Parse the URL and get the path
        parsed_url = urlparse(url)
        path = unquote(parsed_url.path)
        
        # Extract filename from path
        filename = os.path.basename(path)
        
        # If no filename or no extension, generate one
        if not filename or '.' not in filename:
            # Generate filename with timestamp
            timestamp = int(time.time())
            filename = f"image_{timestamp}.jpg"
            print(f"ℹ  Generated filename: {filename}")
        else:
            print(f"ℹ  Using filename from URL: {filename}")
            
        return filename
    
    except Exception as e:
        # Fallback filename generation
        timestamp = int(time.time())
        filename = f"image_{timestamp}.jpg"
        print(f"ℹ  Generated fallback filename: {filename}")
        return filename


def download_image(url, directory):
    """
    Download image from URL and save it to the specified directory.
    Ubuntu principles: Community (web connection), Respect (error handling)
    """
    try:
        print(f"🌐 Connecting to: {url}")
        
        # Set a reasonable timeout and headers to be respectful
        headers = {
            'User-Agent': 'Ubuntu-Image-Downloader/1.0 (Educational Purpose)'
        }
        
        # Make the request with timeout
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Verify content type is an image
        content_type = response.headers.get('content-type', '').lower()
        if not content_type.startswith('image/'):
            print(f"⚠  Warning: Content-Type is '{content_type}', may not be an image")
        
        # Extract filename
        filename = extract_filename_from_url(url)
        filepath = os.path.join(directory, filename)
        
        # Save the image in binary mode
        print(f"💾 Saving image to: {filepath}")
        with open(filepath, 'wb') as f:
            # Download in chunks to handle large files efficiently
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Get file size for confirmation
        file_size = os.path.getsize(filepath)
        print(f"✅ Successfully downloaded {filename} ({file_size:,} bytes)")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Error: Connection timed out. Please check your internet connection or try again later.")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server. Please check the URL and your internet connection.")
        return False
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error: HTTP {e.response.status_code} - {e.response.reason}")
        if e.response.status_code == 404:
            print("   The image was not found at the provided URL.")
        elif e.response.status_code == 403:
            print("   Access to the image is forbidden.")
        elif e.response.status_code >= 500:
            print("   Server error. Please try again later.")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Request failed - {str(e)}")
        return False
        
    except OSError as e:
        print(f"❌ Error: Could not save file - {str(e)}")
        print("   Please check file permissions and disk space.")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def main():
    """
    Main function that orchestrates the image downloading process.
    Ubuntu principle: Practicality - Create a user-friendly interface
    """
    print("🐧 Ubuntu Image Downloader")
    print("=" * 40)
    print("This tool embodies Ubuntu principles:")
    print("• Community: Connects to the web community")
    print("• Respect: Handles errors gracefully")
    print("• Sharing: Organizes images for sharing")
    print("• Practicality: Serves a real need")
    print("=" * 40)
    
    # Create directory
    directory = create_fetched_images_directory()
    
    while True:
        try:
            # Prompt user for URL
            print("\n📝 Please enter the URL of the image you want to download:")
            url = input("URL: ").strip()
            
            # Check if user wants to exit
            if url.lower() in ['quit', 'exit', 'q', '']:
                if url == '':
                    print("Empty URL entered.")
                print("👋 Thank you for using Ubuntu Image Downloader!")
                break
            
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                print("⚠  Please enter a valid URL starting with http:// or https://")
                continue
            
            # Download the image
            success = download_image(url, directory)
            
            if success:
                # Ask if user wants to download another image
                print("\n🔄 Would you like to download another image? (y/n)")
                choice = input("Choice: ").strip().lower()
                if choice not in ['y', 'yes']:
                    print("👋 Thank you for using Ubuntu Image Downloader!")
                    break
            else:
                # Ask if user wants to try again or quit
                print("\n🔄 Would you like to try with a different URL? (y/n)")
                choice = input("Choice: ").strip().lower()
                if choice not in ['y', 'yes']:
                    print("👋 Thank you for using Ubuntu Image Downloader!")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in main program: {str(e)}")
            print("The program will continue running...")


if __name__ == "__main__":
    main()