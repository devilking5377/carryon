#!/usr/bin/env python3
"""
Simple test script for the CarryOn Summary API
"""
import requests
import json

def test_api():
    """Test the Flask API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing CarryOn Summary API...")
    print()
    
    # Test health endpoint (new structure)
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            data = response.json()
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 5000")
        return
    
    # Test API info endpoint
    try:
        response = requests.get(f"{base_url}/api/info")
        if response.status_code == 200:
            print("✅ API info: PASSED")
            data = response.json()
            print(f"   Name: {data.get('name', 'Unknown')}")
        else:
            print(f"❌ API info: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ API info: ERROR - {e}")
    
    # Test summarize endpoint
    test_text = """
    This is a long piece of text that needs to be summarized. It contains multiple sentences
    and various information that should be condensed into a shorter format. The summarizer
    should extract the most important points and create a concise summary that preserves
    the key information while reducing the overall length. This test will help verify
    that the API is working correctly and can process text summarization requests.
    """
    
    try:
        response = requests.post(
            f"{base_url}/api/summarize",
            json={
                "text": test_text,
                "target_sentences": 6
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Summarize API: PASSED")
            print(f"   📝 Original words: {data['meta']['words_total']}")
            print(f"   📄 Summary: {data['summary'][:100]}...")
        else:
            print(f"❌ Summarize API: FAILED ({response.status_code})")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Summarize API: ERROR - {e}")
    
    # Test stats endpoint
    try:
        response = requests.post(
            f"{base_url}/api/stats",
            json={"text": test_text},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Stats API: PASSED")
            print(f"   📊 Words: {data['words_total']}")
            print(f"   📄 Sentences: {data['sentences_total']}")
            print(f"   📋 Paragraphs: {data['paragraphs_total']}")
            print(f"   🎯 Recommended: {data['recommended_target']}")
        else:
            print(f"❌ Stats API: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Stats API: ERROR - {e}")
    
    print()
    print("🎉 API testing complete!")

if __name__ == "__main__":
    test_api()