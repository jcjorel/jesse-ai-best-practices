#!/usr/bin/env python3
"""
Debug test for smart compliance function isolation.
Tests the get_gitignore_compliance_status function directly.
"""

import asyncio
from jesse_framework_mcp.resources.gitignore import get_gitignore_compliance_status
from utils import unwrap_fastmcp_function

class DebugContext:
    async def info(self, msg): print(f"INFO: {msg}")
    async def error(self, msg): print(f"ERROR: {msg}")

async def debug_smart_compliance():
    print("=== DEBUGGING SMART COMPLIANCE ===")
    ctx = DebugContext()
    
    try:
        # Test function import and unwrapping
        print("1. Testing function import...")
        compliance_func = unwrap_fastmcp_function(get_gitignore_compliance_status)
        print("✅ Function imported and unwrapped successfully")
        
        # Test function execution
        print("2. Testing function execution...")
        result = await compliance_func(ctx)
        print(f"✅ Function executed successfully")
        print(f"📊 Result type: {type(result)}")
        print(f"📊 Result length: {len(result)} chars")
        print(f"📊 Result preview: {repr(result[:200])}")
        
        if result.strip():
            print("⚠️ Compliance issues detected - function returned content")
        else:
            print("✅ No compliance issues - function returned empty string")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in smart compliance: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(debug_smart_compliance())
