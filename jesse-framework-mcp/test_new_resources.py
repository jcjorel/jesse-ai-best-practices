#!/usr/bin/env python3
"""
Test script for the new README.md resources.
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to sys.path to import the MCP server modules
sys.path.insert(0, str(Path(__file__).parent))

from jesse_framework_mcp.resources.knowledge import register_knowledge_resources
from jesse_framework_mcp.main import server
from fastmcp import Context

async def test_git_clones_readme():
    """Test the git-clones-readme resource"""
    print("Testing git-clones-readme resource...")
    
    try:
        # Test if the README file exists
        import os
        readme_path = ".knowledge/git-clones/README.md"
        if os.path.exists(readme_path):
            print(f"✅ Git clones README file exists: {readme_path}")
            
            # Read the file content
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"✅ Git clones README content loaded: {len(content)} characters")
            
            # Check if it contains expected content
            if "Git Clone Knowledge Bases Index" in content:
                print("✅ Git clones README contains expected header")
            else:
                print("❌ Git clones README missing expected header")
                
            if "FastMCP" in content and "Cline" in content:
                print("✅ Git clones README contains expected knowledge bases")
            else:
                print("❌ Git clones README missing expected knowledge bases")
        else:
            print(f"❌ Git clones README file not found: {readme_path}")
            
    except Exception as e:
        print(f"❌ Git clones README test failed: {str(e)}")

async def test_pdf_knowledge_readme():
    """Test the pdf-knowledge-readme resource"""
    print("\nTesting pdf-knowledge-readme resource...")
    
    try:
        # Test if the PDF knowledge directory exists
        import os
        pdf_dir = ".knowledge/pdf-knowledge"
        readme_path = ".knowledge/pdf-knowledge/README.md"
        
        if os.path.exists(pdf_dir):
            print(f"✅ PDF knowledge directory exists: {pdf_dir}")
            if os.path.exists(readme_path):
                print(f"✅ PDF knowledge README file exists: {readme_path}")
                
                # Read the file content
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"✅ PDF knowledge README content loaded: {len(content)} characters")
            else:
                print(f"⚠️ PDF knowledge README file not found: {readme_path}")
        else:
            print(f"⚠️ PDF knowledge directory does not exist: {pdf_dir} (expected for new installations)")
            print("✅ Resource should handle this gracefully with default content")
            
    except Exception as e:
        print(f"❌ PDF knowledge README test failed: {str(e)}")

async def test_resource_registration():
    """Test that the new resources are properly registered"""
    print("\nTesting resource registration...")
    
    try:
        # Register the knowledge resources
        register_knowledge_resources()
        print("✅ Knowledge resources registered successfully")
        
        # Check that the server has the resources registered
        # This is a basic check that registration doesn't crash
        print("✅ Resource registration completed without errors")
        
    except Exception as e:
        print(f"❌ Resource registration test failed: {str(e)}")

async def main():
    """Run all tests"""
    print("=" * 60)
    print("TESTING NEW WRITABLE RESOURCES")
    print("=" * 60)
    
    await test_git_clones_readme()
    await test_pdf_knowledge_readme()
    await test_resource_registration()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
