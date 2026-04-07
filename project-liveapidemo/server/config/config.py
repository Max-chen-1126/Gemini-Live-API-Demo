# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Configuration for Gemini Live API Server
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables (search current dir and parent dir, override system env vars)
load_dotenv(override=True)
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env", override=True)


class ConfigurationError(Exception):
    """Custom exception for configuration errors."""


class ApiConfig:
    """API configuration handler."""

    def __init__(self):
        self.api_key = None
        self.maps_api_key = None
        logger.info("Initialized API configuration for Google AI Studio")

    async def initialize(self):
        """Initialize API credentials."""
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ConfigurationError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable is required")
        self.maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.maps_api_key:
            logger.warning("GOOGLE_MAPS_API_KEY not set - Google Maps tools will not work")
        self.maps_js_api_key = os.getenv("GOOGLE_MAPS_JS_API_KEY", self.maps_api_key)
        if not self.maps_js_api_key:
            logger.warning("GOOGLE_MAPS_JS_API_KEY not set - frontend map will not work")


# Initialize API configuration
api_config = ApiConfig()

# Model configuration
MODEL = "models/gemini-3.1-flash-live-preview"
VOICE = os.getenv("VOICE", "Kore")


# Load system instructions
try:
    with open("config/system-instructions.txt", "r") as f:
        SYSTEM_INSTRUCTIONS = f.read()
except Exception as e:
    logger.error(f"Failed to load system instructions: {e}")
    SYSTEM_INSTRUCTIONS = ""

logger.info(f"System instructions: {SYSTEM_INSTRUCTIONS}")

# Google Maps Function Declarations
MAPS_FUNCTION_DECLARATIONS = {
    "function_declarations": [
        {
            "name": "compute_route",
            "description": "規劃從起點到目的地的路線。當使用者提到想去某個地方、詢問路線、距離、時間、怎麼去、怎麼走時，必須呼叫此工具取得距離、時間和路線資訊。絕不可自行編造路線數據。",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "origin": {
                        "type": "STRING",
                        "description": "起點地址或地名，例如：台北車站、台中市",
                    },
                    "destination": {
                        "type": "STRING",
                        "description": "目的地地址或地名，例如：九份老街、日月潭",
                    },
                    "travel_mode": {
                        "type": "STRING",
                        "description": "交通方式，預設 DRIVE",
                        "enum": ["DRIVE", "TRANSIT", "WALK", "BICYCLE"],
                    },
                },
                "required": ["origin", "destination"],
            },
        },
        {
            "name": "search_places_along_route",
            "description": "搜尋路線沿途的景點、餐廳或其他地點。需先呼叫 compute_route 取得路線後使用。結果會均勻分佈在路線上。如果使用者指定了特定區域（如「在內湖找餐廳」），請用 focus_location 參數指定該區域。",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "搜尋關鍵字，如：景點、餐廳、休息站、觀光",
                    },
                    "route_polyline": {
                        "type": "STRING",
                        "description": "從 compute_route 回傳結果中取得的 encoded polyline 字串",
                    },
                    "focus_location": {
                        "type": "STRING",
                        "description": "可選。指定搜尋重點區域的地名，例如：內湖、新竹、苗栗。不指定時結果會均勻分佈在整條路線上。",
                    },
                },
                "required": ["query", "route_polyline"],
            },
        },
        {
            "name": "search_nearby_places",
            "description": "搜尋某地點附近的景點、餐廳或設施",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "搜尋關鍵字，如：景點、美食、咖啡廳",
                    },
                    "latitude": {
                        "type": "NUMBER",
                        "description": "搜尋中心點的緯度",
                    },
                    "longitude": {
                        "type": "NUMBER",
                        "description": "搜尋中心點的經度",
                    },
                    "radius_meters": {
                        "type": "NUMBER",
                        "description": "搜尋半徑（公尺），預設 5000",
                    },
                },
                "required": ["query", "latitude", "longitude"],
            },
        },
    ]
}

# Gemini Configuration
CONFIG = {
    "generation_config": {
        "response_modalities": ["AUDIO"],
        "speech_config": {
            "voice_config": {"prebuilt_voice_config": {"voice_name": VOICE}},
            "language_code": "cmn-CN",
        },
    },
    "input_audio_transcription": {},
    "output_audio_transcription": {},
    "tools": [{"google_search": {}}, MAPS_FUNCTION_DECLARATIONS],
    "system_instruction": SYSTEM_INSTRUCTIONS,
}
