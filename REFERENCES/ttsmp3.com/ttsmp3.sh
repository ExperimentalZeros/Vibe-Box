#!/usr/bin/bash

# 1. Remove spaces around '=' and quote the variables
voice="$1"
message="$2"

# Optional but recommended: Check if the user actually provided both arguments
if [ -z "$voice" ] || [ -z "$message" ]; then
    echo "Usage: $0 <voice> \"<message>\""
    echo "Example: $0 Lupe \"Hello, this is a test.\""
    exit 1
fi

# 2. Use --data-urlencode for the message so spaces/special characters don't break the request
curl -s -X POST https://ttsmp3.com/makemp3_new.php \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "msg=$message" \
  -d "lang=$voice" \
  -d "source=ttsmp3" | jq -r .URL | xargs curl -s -o "$(date +%s)_${voice}_${message}.mp3"
