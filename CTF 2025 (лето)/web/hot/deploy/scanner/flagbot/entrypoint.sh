#!/bin/sh

while true; do
    curl -s 'http://gotenberg:3000/forms/chromium/convert/html' --form 'files=@"index.html"' -o ./output.pdf
    sleep 5
done