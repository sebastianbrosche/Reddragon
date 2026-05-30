#!/bin/bash
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -i ~/.ssh/localhost_run_key -R 80:localhost:8000 localhost.run sleep 300 > /tmp/localhost_run.log 2>&1 &
echo $! > /tmp/localhost_run.pid
sleep 5
grep -E "(https?://[a-z0-9-]+\.lhr\.life|https?://[a-z0-9-]+\.localhost\.run)" /tmp/localhost_run.log | head -1