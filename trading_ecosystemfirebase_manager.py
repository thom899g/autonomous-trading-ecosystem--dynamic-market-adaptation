"""
Firebase Firestore manager for real-time state management and data persistence.
Implements CRUD operations with robust error handling and connection management.
"""
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import asyncio

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.api_core.exceptions import GoogleAPICallError, RetryError

from .config import config

logger = logging.getLogger(__name__)


class FirebaseManager:
    """Manages Firebase Firestore connections and operations"""
    
    def __init__(self):
        self._app = None
        self._client: Optional[FirestoreClient] = None
        self._is_connected = False
        
        logger.info("Initializing Firebase Manager")
        self._initialize_firebase()
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection with error handling"""
        try:
            if config.firebase_config.credentials_path:
                cred = credentials.Certificate(config.firebase_config.credentials_path)
                self._app = firebase_admin.initialize_app(cred)
            else:
                # Use default credentials (GOOGLE_APPLICATION_CREDENTIALS env var)
                self._app = firebase_admin