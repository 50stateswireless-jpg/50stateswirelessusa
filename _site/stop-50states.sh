#!/bin/bash

# Use the command you verified works, adding 'ruby' just to be safe 
# and the -9 flag to force an immediate stop.
pkill -9 -f "jekyll|decap-server|ruby"

# We don't need a sleep or echo here because we want it to 
# execute the command and finish instantly.
exit 0
