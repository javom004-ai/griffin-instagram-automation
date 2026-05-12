#!/usr/bin/env python3
"""
Griffin Instagram Scheduler
Automatiza publicaciones en Instagram/Meta Business usando Graph API
"""

import requests
import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GriffinScheduler:
    def __init__(self, access_token: str, business_account_id: str):
        self.access_token = access_token
        self.business_account_id = business_account_id
        self.base_url = "https://graph.instagram.com/v18.0"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })
    
    def schedule_reel(self, video_url: str, caption: str, hashtags: str, publish_time: str):
        """Programa un Reel para publicación"""
        payload = {
            "video_url": video_url,
            "caption": f"{caption}\n\n{hashtags}",
            "access_token": self.access_token,
            "scheduled_publish_time": datetime.fromisoformat(publish_time).timestamp()
        }
        
        url = f"{self.base_url}/{self.business_account_id}/media"
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Reel programado: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error programando reel: {e}")
            return {"error": str(e)}
    
    def batch_schedule_from_csv(self, csv_file: str):
        """Programa posts desde CSV con formato: date,format,copy,hashtags,image_urls"""
        import csv
        results = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    publish_time = f"{row['date']}T10:00:00"
                    result = self.schedule_reel(
                        video_url=row['image_urls'],
                        caption=row['copy'],
                        hashtags=row['hashtags'],
                        publish_time=publish_time
                    )
                    results.append(result)
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {csv_file}")
        
        return results

if __name__ == "__main__":
    access_token = os.getenv("META_ACCESS_TOKEN")
    business_account_id = os.getenv("META_BUSINESS_ACCOUNT_ID")
    scheduler = GriffinScheduler(access_token, business_account_id)
    print("Griffin Scheduler iniciado")
