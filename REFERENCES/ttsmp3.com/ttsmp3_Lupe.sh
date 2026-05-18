curl -s -X POST https://ttsmp3.com/makemp3_new.php \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "msg=Hello, this is a direct terminal download." \
  -d "lang=Lupe" \
  -d "source=ttsmp3" | jq -r .URL | xargs curl -s -O
