#!/usr/bin/env python3
"""
LegalX Data Setup Script
========================

This script helps you set up and manage the legal document data for LegalX.

Usage:
    python setup_data.py

Functions:
- Check existing data files
- Validate data integrity
- Provide instructions for adding new documents
- Rebuild vector store if needed
"""

import os
import json
import sys
from pathlib import Path

def check_data_files():
    """Check if required data files exist."""
    data_dir = Path("data")
    required_files = [
        "ipc_sections_cleaned.json",
        "ipc_sections_formatted.pdf",
        "Cyber Crimes Offenses & Penalties In India[1].pdf"
    ]

    print("📁 Checking data files...")
    all_present = True

    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} - MISSING")
            all_present = False

    return all_present

def validate_json_data():
    """Validate the JSON data file."""
    json_path = Path("data/ipc_sections_cleaned.json")

    if not json_path.exists():
        print("❌ JSON data file not found")
        return False

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list) and len(data) > 0:
            print(f"✅ JSON data valid: {len(data)} entries")
            return True
        else:
            print("❌ JSON data is empty or invalid format")
            return False

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        return False

def show_usage_instructions():
    """Show instructions for using the data."""
    print("\n📖 Usage Instructions:")
    print("=" * 50)
    print("1. 📄 Current Data Files:")
    print("   - ipc_sections_cleaned.json: Processed legal sections")
    print("   - ipc_sections_formatted.pdf: Formatted IPC sections")
    print("   - Cyber Crimes...: Cyber crime laws and penalties")
    print()
    print("2. 🆕 Adding New Documents:")
    print("   - Place PDF files in the 'data/' directory")
    print("   - Run: python built_vector_store.py")
    print("   - The system will automatically process new PDFs")
    print()
    print("3. 🔄 Rebuilding Vector Store:")
    print("   - Delete the 'chroma_store/' directory")
    print("   - Run: python built_vector_store.py")
    print()
    print("4. 🚀 Running the Application:")
    print("   - Backend: python api_2.py")
    print("   - Frontend: cd workspace && npm run dev")

def main():
    """Main setup function."""
    print("🤖 LegalX Data Setup")
    print("=" * 30)

    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Check data files
    data_ok = check_data_files()
    print()

    # Validate JSON data
    json_ok = validate_json_data()
    print()

    # Show results
    if data_ok and json_ok:
        print("🎉 Data setup complete! All files are present and valid.")
        print("You can now run: python built_vector_store.py")
    else:
        print("⚠️  Some data files are missing or invalid.")
        print("Please ensure all required files are in the data/ directory.")

    # Show usage instructions
    show_usage_instructions()

    return data_ok and json_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)