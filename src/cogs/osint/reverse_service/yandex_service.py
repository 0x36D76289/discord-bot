# cogs/utils/services/yandex_service.py
import aiohttp
from bs4 import BeautifulSoup
import re
import json

class YandexService:
    def __init__(self):
        self.base_url = "https://yandex.com/images/search"

    async def search_image(self, image_url=None, filepath=None):
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        if image_url:
            url = f"{self.base_url}?rpt=imageview&url={image_url}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    content = await response.text()
        else:
            return []

        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all script tags
        script_tags = soup.find_all('script')

        for script in script_tags:
            if script.string:
                if 'data-state' in script.string:
                    data_state = script.string
                    break
                
        # Extract the JSON data
        json_data = data_state.split('data-state="', 1)[1].split('">', 1)[0]
        decoded_data = json.loads(json_data)
        
        results = []
        
        for item in decoded_data['sites']:
            results.append({
                "service": "Yandex Images",
                "url": item["url"],
                "page_url": item["domain"]
            })

        return results[:3]