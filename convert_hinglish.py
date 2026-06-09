#!/usr/bin/env python3
"""
ITI Hinglish to English Converter
Converts all Hinglish questions in Q_DB to pure English
"""

import re
import json
from pathlib import Path

# Comprehensive Hinglish to English mapping
HINGLISH_DICT = {
    # Generic question patterns
    r"kya hai\?": "?",
    r"kya hota hai\?": "?",
    r"ka kaam kya hai\?": "'s function?",
    r"ka matlab kya hai\?": " mean?",
    r"ka full form kya hai\?": "'s full form?",
    r"ka pura naam kya hai\?": "'s full name?",
    r"kaun sa hota hai\?": "?",
    r"kahan hota hai\?": "?",
    r"kahan use hota hai\?": " used?",
    r"kyun karte hain\?": "?",
    r"kyun use karte hain\?": " used?",
    r"kyun important hai\?": " important?",
    r"kyun zaroori hai\?": " necessary?",
    r"kaise set karte hain\?": " set?",
    r"kaise karte hain\?": " done?",
    r"mein kya fark hai\?": " difference?",
    r"aur": "and",
    r"hai": "is",
    r"ek": "a/an",
    
    # Specific conversions (more precise)
    "Computer ka full form": "Full form of Computer",
    "CPU ka full form": "Full form of CPU",
    "RAM ka pura naam": "Full name of RAM",
    "1 GB mein kitne MB": "How many MB in 1 GB",
    "Input device ka": "What is an input device",
    "Computer ki speed": "Computer speed measurement",
    "Primary memory": "Primary memory",
    "Hard Disk Drive (HDD) kiska": "Hard Disk Drive (HDD) is an example of",
    "Binary number system ka": "Binary number system",
    "1 Byte mein kitne": "How many bits in 1 Byte",
    "Operating System ka": "Operating System",
    "MS Word mein": "in MS Word",
    "MS Excel mein": "in MS Excel",
    "Windows mein": "in Windows",
    "MS PowerPoint mein": "in MS PowerPoint",
    "Recycle Bin mein": "in Recycle Bin",
    "Windows Explorer mein": "in Windows Explorer",
    "WWW ka": "WWW",
    "HTTP ka": "HTTP",
    "Secure websites": "Secure websites",
    "Email mein CC": "CC in email",
    "LAN ka": "LAN",
    "IP Address": "IP Address",
    "DNS ka": "DNS",
    "Wi-Fi ka": "Wi-Fi",
    "Phishing attack": "Phishing attack",
    "Cloud storage": "Cloud storage",
    "Programming language": "Programming language",
    "Database ka": "Database",
    "SQL ka": "SQL",
    "Variable": "Variable",
    "Loop": "Loop",
    "HTML ka": "HTML",
    "Primary Key": "Primary Key",
    "Algorithm": "Algorithm",
    "Binary search": "Binary search",
    
    # Electrical terms
    "Ohm's Law ke anusar": "According to Ohm's Law",
    "Current ki unit": "Unit of current",
    "Electrical safety mein sabse pehla": "First rule of electrical safety",
    "Resistance ki unit": "Unit of resistance",
    "Short circuit": "Short circuit",
    "Earthing ka": "Earthing",
    "Fuse": "Fuse",
    "India mein AC supply ki standard": "Standard AC frequency in India",
    "PPE mein rubber gloves": "Rubber gloves in PPE",
    "Voltmeter circuit": "Voltmeter in circuit",
    "New Indian standard mein Live": "Live wire color in new Indian standard",
    "3-pin plug mein sabse": "3-pin plug largest pin",
    "MCB ka": "MCB",
    "House wiring mein ring": "Ring main circuit in house wiring",
    "Two-way switch": "Two-way switch",
    "ELCB ka": "ELCB",
    "PVC wire ka": "PVC wire",
    "Wire gauge number": "Wire gauge",
    "Switch": "Switch in circuit",
    "Star (Y) connection": "Star connection",
    
    # Fitter terms
    "Bench vice ka": "Bench vice",
    "Try square": "Try square",
    "Scriber": "Scriber",
    "Centre punch": "Centre punch",
    "Layout dye": "Layout dye (Prussian Blue)",
    "Surface plate": "Surface plate",
    "Filing": "Filing",
    "Chipping": "Chipping",
    "Straight rule": "Straight rule",
    "Angle plate": "Angle plate",
}

def convert_hinglish_to_english(text):
    """Convert Hinglish text to English"""
    if not text:
        return text
    
    conversions = [
        # High-priority specific phrases
        ("ka full form kya hai?", "'s full form?"),
        ("ka pura naam kya hai?", "'s full name?"),
        ("ka kaam kya hai?", "'s function/purpose?"),
        ("ka matlab kya hai?", " mean?"),
        ("kya hai?", "?"),
        ("kya hota hai?", "?"),
        ("kahan hota hai?", "?"),
        ("kyun karte hain?", "?"),
        ("kaise karte hain?", " done?"),
        ("mein kya fark hai?", " difference?"),
        ("aur", "and"),
    ]
    
    result = text
    for hinglish, english in conversions:
        result = result.replace(hinglish, english)
    
    return result

def extract_and_convert_questions(html_content):
    """Extract Q_DB and convert all questions"""
    
    # Find Q_DB section
    qdb_start = html_content.find("const Q_DB = {")
    if qdb_start == -1:
        print("❌ Could not find Q_DB section")
        return html_content
    
    qdb_end = html_content.find("\n};", qdb_start) + 3
    qdb_section = html_content[qdb_start:qdb_end]
    
    # Find all questions with q:' pattern
    pattern = r"q:'([^']*)'|q:\"([^\"]*)\""
    
    def replace_question(match):
        # Get the actual text (group 1 or 2)
        text = match.group(1) or match.group(2)
        
        # Skip if already in English (rough check)
        if text.lower().startswith(('what', 'which', 'where', 'when', 'how', 'why', 'is ', 'are ', 'to', 'the')):
            return match.group(0)
        
        # Convert Hinglish to English
        converted = convert_hinglish_to_english(text)
        
        # Return with proper quote
        quote_type = "'" if match.group(1) else '"'
        return f"q:{quote_type}{converted}{quote_type}"
    
    # Replace in Q_DB section
    converted_qdb = re.sub(pattern, replace_question, qdb_section)
    
    # Replace in full content
    converted_html = html_content[:qdb_start] + converted_qdb + html_content[qdb_end:]
    
    return converted_html

def convert_generic_banks(html_content):
    """Convert GENERIC_Q_BANKS questions"""
    
    banks_start = html_content.find("const GENERIC_Q_BANKS = {")
    if banks_start == -1:
        print("⚠️  Could not find GENERIC_Q_BANKS section")
        return html_content
    
    banks_end = html_content.find("\n};", banks_start) + 3
    banks_section = html_content[banks_start:banks_end]
    
    # Find all questions
    pattern = r"q:'([^']*)'|q:\"([^\"]*)\""
    
    def replace_question(match):
        text = match.group(1) or match.group(2)
        
        if text.lower().startswith(('what', 'which', 'where', 'when', 'how', 'why', 'is ', 'are ', 'to', 'the')):
            return match.group(0)
        
        converted = convert_hinglish_to_english(text)
        quote_type = "'" if match.group(1) else '"'
        return f"q:{quote_type}{converted}{quote_type}"
    
    converted_banks = re.sub(pattern, replace_question, banks_section)
    converted_html = html_content[:banks_start] + converted_banks + html_content[banks_end:]
    
    return converted_html

def convert_unique_questions(html_content):
    """Convert TRADE_UNIQUE_QS questions"""
    
    unique_start = html_content.find("const TRADE_UNIQUE_QS = {")
    if unique_start == -1:
        print("⚠️  Could not find TRADE_UNIQUE_QS section")
        return html_content
    
    unique_end = html_content.find("\n};", unique_start) + 3
    unique_section = html_content[unique_start:unique_end]
    
    pattern = r"q:'([^']*)'|q:\"([^\"]*)\""
    
    def replace_question(match):
        text = match.group(1) or match.group(2)
        
        if text.lower().startswith(('what', 'which', 'where', 'when', 'how', 'why', 'is ', 'are ', 'to', 'the')):
            return match.group(0)
        
        converted = convert_hinglish_to_english(text)
        quote_type = "'" if match.group(1) else '"'
        return f"q:{quote_type}{converted}{quote_type}"
    
    converted_unique = re.sub(pattern, replace_question, unique_section)
    converted_html = html_content[:unique_start] + converted_unique + html_content[unique_end:]
    
    return converted_html

def main():
    print("=" * 60)
    print("🔄 ITI Hinglish to English Converter")
    print("=" * 60)
    
    file_path = Path("index.html")
    
    if not file_path.exists():
        print("❌ index.html not found!")
        return
    
    print(f"📂 Reading: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    original_size = len(original_content)
    print(f"📊 Original file size: {original_size:,} bytes")
    
    # Count Hinglish questions
    hinglish_count = len(re.findall(r"q:'[^']*([का|की|को|से|में|या|है|हो|कर|ध्|ज्|छ|ञ|ड|ण|त|थ|द|ध|न|प|फ|ब|भ|म|य|र|ल|व|श|ष|स|ह][^']*)'", original_content))
    print(f"🔍 Found approximately {hinglish_count} Hinglish questions")
    
    # Convert all sections
    print("\n🔄 Converting Q_DB questions...")
    converted_content = extract_and_convert_questions(original_content)
    
    print("🔄 Converting GENERIC_Q_BANKS...")
    converted_content = convert_generic_banks(converted_content)
    
    print("🔄 Converting TRADE_UNIQUE_QS...")
    converted_content = convert_unique_questions(converted_content)
    
    # Backup original
    backup_path = Path("index.html.backup")
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"\n✅ Backup created: {backup_path}")
    
    # Write converted content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(converted_content)
    
    converted_size = len(converted_content)
    print(f"✅ Converted file saved: {file_path}")
    print(f"📊 New file size: {converted_size:,} bytes")
    print(f"📈 Size difference: {abs(converted_size - original_size):,} bytes")
    
    print("\n" + "=" * 60)
    print("✅ Conversion Complete!")
    print("=" * 60)
    print("\n📋 Summary:")
    print("   • Q_DB questions: Converted")
    print("   • GENERIC_Q_BANKS: Converted")
    print("   • TRADE_UNIQUE_QS: Converted")
    print("\n⚠️  Note: Backup saved as index.html.backup")
    print("💡 Review the results and run manual fixes if needed")

if __name__ == "__main__":
    main()
