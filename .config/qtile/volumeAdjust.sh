#!/usr/bin/env bash

step=5
if [[ $# -eq 1 ]]; then
    case $1 in 
        "up")
            amixer -M -c 0 set Master $step+;;
        "down")
            amixer -M -c 0 set Master $step-;;
        "toggle")
            amixer -M -c 0 set Master playback toggle
            amixer -M -c 0 set Headphone playback unmute
            amixer -M -c 0 set Front playback unmute
            amixer -M -c 0 set Speaker playback unmute
            ;;
        *)
            echo "Invalid option";;
    esac
fi