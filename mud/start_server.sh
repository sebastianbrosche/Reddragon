#!/bin/bash
cd /root/.openclaw/workspace/mud/madamsir_mud
source ../evenv/bin/activate
evennia migrate
evennia start