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

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ConfigurationError(Exception):
    """Custom exception for configuration errors."""


class ApiConfig:
    """API configuration handler."""

    def __init__(self):
        self.api_key = None
        logger.info("Initialized API configuration for Google AI Studio")

    async def initialize(self):
        """Initialize API credentials."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ConfigurationError(
                "GOOGLE_API_KEY environment variable is required"
            )


# Initialize API configuration
api_config = ApiConfig()

# Model configuration
MODEL = os.getenv("MODEL", "models/gemini-2.0-flash-exp")
VOICE = os.getenv("VOICE", "Kore")


# Load system instructions
try:
    with open("config/system-instructions.txt", "r") as f:
        SYSTEM_INSTRUCTIONS = f.read()
except Exception as e:
    logger.error(f"Failed to load system instructions: {e}")
    SYSTEM_INSTRUCTIONS = ""

logger.info(f"System instructions: {SYSTEM_INSTRUCTIONS}")

# Gemini Configuration
CONFIG = {
    "generation_config": {
        "response_modalities": ["AUDIO"],
        "speech_config": {
            "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}},
            "language_code": "cmn-CN",
        },
    },
    "tools": [{"google_search": {}}],
    "system_instruction": SYSTEM_INSTRUCTIONS,
}
