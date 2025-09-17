#!/usr/bin/env python3
"""
Simple startup test script for Railway deployment debugging.
This script tests if the MCP Atlassian server can start with minimal configuration.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_startup():
    """Test that the server can start up properly."""
    try:
        # Set minimal environment variables
        os.environ["TRANSPORT"] = "sse"
        os.environ["HOST"] = "0.0.0.0" 
        os.environ["PORT"] = "8000"
        os.environ["MCP_LOGGING_STDOUT"] = "true"
        os.environ["MCP_VERBOSE"] = "true"
        
        print("🔧 Testing MCP Atlassian server startup...")
        print(f"Transport: {os.environ.get('TRANSPORT')}")
        print(f"Host: {os.environ.get('HOST')}")
        print(f"Port: {os.environ.get('PORT')}")
        
        # Import and test the server
        from mcp_atlassian.servers import main_mcp
        
        print("✅ Successfully imported main_mcp")
        
        # Test that we can access the FastMCP instance
        print(f"✅ Server name: {main_mcp.name}")
        print(f"✅ Server type: {type(main_mcp)}")
        
        # Try to start the server for a brief moment
        print("🚀 Attempting to start server (will timeout after 5 seconds)...")
        
        try:
            await asyncio.wait_for(
                main_mcp.run_async(
                    transport="sse",
                    host="0.0.0.0",
                    port=8000,
                    log_level="debug"
                ),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            print("✅ Server started successfully (timed out as expected)")
            return True
        except Exception as e:
            print(f"❌ Server failed to start: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test startup: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_startup())
    sys.exit(0 if success else 1)