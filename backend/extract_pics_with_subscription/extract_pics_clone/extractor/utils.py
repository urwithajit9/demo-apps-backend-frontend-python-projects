import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from PIL import Image as PILImage
import io
import os
from .models import Image, Extraction


def extract_images_from_url(url, extraction_obj):
    """
    Extract images from a given URL and save them to the database.
    """
    try:
        # Update extraction status
        extraction_obj.status = 'processing'
        extraction_obj.save()
        
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all image elements
        img_tags = soup.find_all('img')
        
        # Extract images from various sources
        image_urls = set()
        
        # Regular img tags
        for img in img_tags:
            src = img.get('src')
            if src:
                full_url = urljoin(url, src)
                image_urls.add(full_url)
        
        # Background images from CSS
        css_images = extract_css_background_images(response.text, url)
        image_urls.update(css_images)
        
        # SVG elements
        svg_tags = soup.find_all('svg')
        for svg in svg_tags:
            # For SVG, we'll store the SVG content as a data URL
            svg_content = str(svg)
            if svg_content and len(svg_content) < 10000:  # Limit SVG size
                data_url = f"data:image/svg+xml;base64,{svg_content.encode('utf-8').hex()}"
                image_urls.add(data_url)
        
        # Process each image URL
        processed_count = 0
        for img_url in image_urls:
            try:
                image_info = get_image_info(img_url, headers)
                if image_info:
                    # Create Image object
                    Image.objects.create(
                        extraction=extraction_obj,
                        url=img_url,
                        name=image_info.get('name', ''),
                        width=image_info.get('width'),
                        height=image_info.get('height'),
                        file_size=image_info.get('file_size'),
                        file_type=image_info.get('file_type', ''),
                        alt_text=image_info.get('alt_text', '')
                    )
                    processed_count += 1
                    
                    # Limit to prevent too many images
                    if processed_count >= 100:
                        break
                        
            except Exception as e:
                print(f"Error processing image {img_url}: {str(e)}")
                continue
        
        # Update extraction status
        extraction_obj.status = 'completed'
        extraction_obj.save()
        
        return processed_count
        
    except Exception as e:
        extraction_obj.status = 'failed'
        extraction_obj.error_message = str(e)
        extraction_obj.save()
        raise


def extract_css_background_images(html_content, base_url):
    """
    Extract background images from CSS in HTML content.
    """
    image_urls = set()
    
    # Find CSS background-image properties
    css_pattern = r'background-image\s*:\s*url\(["\']?([^"\']+)["\']?\)'
    matches = re.findall(css_pattern, html_content, re.IGNORECASE)
    
    for match in matches:
        full_url = urljoin(base_url, match)
        image_urls.add(full_url)
    
    return image_urls


def get_image_info(img_url, headers):
    """
    Get information about an image from its URL.
    """
    try:
        # Skip data URLs for now (except SVG)
        if img_url.startswith('data:') and 'svg' not in img_url:
            return None
            
        # For regular URLs, try to fetch image info
        if not img_url.startswith('data:'):
            response = requests.head(img_url, headers=headers, timeout=10)
            
            # If HEAD doesn't work, try GET with limited content
            if response.status_code != 200:
                response = requests.get(img_url, headers=headers, timeout=10, stream=True)
                # Read only first 1KB to get image info
                content = response.raw.read(1024)
                response.close()
            else:
                content = None
        else:
            content = None
            response = None
        
        # Extract filename from URL
        parsed_url = urlparse(img_url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = 'image'
        
        # Get file extension and type
        file_ext = os.path.splitext(filename)[1].lower().lstrip('.')
        if not file_ext and response:
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                file_ext = 'jpg'
            elif 'png' in content_type:
                file_ext = 'png'
            elif 'gif' in content_type:
                file_ext = 'gif'
            elif 'webp' in content_type:
                file_ext = 'webp'
            elif 'svg' in content_type:
                file_ext = 'svg'
        
        # Get file size
        file_size = None
        if response and 'content-length' in response.headers:
            try:
                file_size = int(response.headers['content-length'])
            except ValueError:
                pass
        
        # Try to get image dimensions (for non-SVG images)
        width, height = None, None
        if content and file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            try:
                img = PILImage.open(io.BytesIO(content))
                width, height = img.size
            except Exception:
                pass
        
        return {
            'name': filename,
            'width': width,
            'height': height,
            'file_size': file_size,
            'file_type': file_ext,
            'alt_text': ''
        }
        
    except Exception as e:
        print(f"Error getting image info for {img_url}: {str(e)}")
        return None

