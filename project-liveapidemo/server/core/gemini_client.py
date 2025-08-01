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
Gemini client initialization and connection management
"""

import logging

from config.config import CONFIG, MODEL, ConfigurationError, api_config
from google import genai

logger = logging.getLogger(__name__)


async def create_gemini_session():
    """Create and initialize the Gemini client and session"""
    try:
        # Initialize authentication
        await api_config.initialize()

        # Initialize development client with Google AI Studio API Key
        logger.info("Initializing Google AI Studio client")

        client = genai.Client(
            http_options={"api_version": "v1alpha"},  # 很多功能 v1alpha
            api_key=api_config.api_key,
        )

        # Create the session
        session = client.aio.live.connect(model=MODEL, config=CONFIG)

        return session

    except ConfigurationError as e:
        logger.error(f"Configuration error while creating Gemini session: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating Gemini session: {str(e)}")
        raise
