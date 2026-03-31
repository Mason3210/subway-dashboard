# Vercel Python Runtime Configuration
# This file is required for Vercel deployment

import vercel
from app import app as application

vercel.app = application
