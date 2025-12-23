#!/bin/bash

# shellcheck disable=SC1091
source ./config.sh

stop_reader ()  {
    pgrep audiobook | sudo xargs kill 2> /dev/null
    pgrep mbrola | sudo xargs kill 2> /dev/null
    pgrep aplay | sudo xargs kill 2> /dev/null
    echo "reader stopped reading"
    audiobook-for-grandma --stop 
}

button_A ()  {
    echo A
    stop_reader
}

button_B ()  {
    echo "B: audiobook-for-grandma --start --language $LANGUAGE --rate $RATE --volume $VOLUME --voice $VOICE >> log/start.log &"
    audiobook-for-grandma --start --language fr --rate "$RATE" --volume "$VOLUME" --voice "$VOICE" >> log/start.log &
    echo "starting"
}

button_X ()  {
    echo X
}

button_Y ()  {
    echo Y
}

button_L1 ()  {
    echo L1
}

button_L2 ()  {
    echo L2
}

button_R1 ()  {
    echo R1
}

button_R2 ()  {
    echo R2
}

button_LEFT ()  {
    echo LEFT
    audiobook-for-grandma --slower
    echo "OK"
}

button_RIGHT ()  {
    echo RIGHT
    audiobook-for-grandma --faster
    echo "OK"
}

button_DOWN ()  {
    echo DOWN
    audiobook-for-grandma --lower
    echo "OK"
}

button_UP ()  {
    echo UP
    audiobook-for-grandma --higher
    echo "OK"
}

button_START ()  {
    echo START
}

button_SELECT ()  {
    echo SELECT
    audiobook-for-grandma --skip 
    echo "OK"
}

button_HOME () {
    echo HOME
}

button_unknow () {
    echo "unknow action $1 for button $2"
}

parse_8BitDo_USB_data () {
    if [ -e "$USB_8BITDO_FILE" ]; then
        echo "$USB_8BITDO_FILE exists."
        (jstest --event "$USB_8BITDO_FILE" || true) | while read -r usb_data; do
            read_usb_data "$usb_data"
        done
    #else
        #echo "The file $USB_8BITDO_FILE does not exists (device not connected). "
    fi
    sleep 1
    parse_8BitDo_USB_data
}

read_usb_data () {
    #press 'A'
    #Event: type 1, time 19564951, number 1, value 1
    regex='Event: type ([[:alnum:]]{1,20}), time ([[:alnum:]]{1,20}), number ([[:alnum:]]{1,20}), value (-?[[:alnum:]]{1,20})'
    if [[ $1 =~ $regex ]]; then
        action="${BASH_REMATCH[1]}"
        button="${BASH_REMATCH[3]}"
        value="${BASH_REMATCH[4]}"
        echo "action : $action ; button : $button ; value : $value"
        case "$action" in
            1)
                case "$value" in
                    1) #press
                        case "$button" in
                            0)
                                button_B;;
                            1)
                                button_A;;
                            2)
                                button_Y;;
                            3)
                                button_X;;
                            4)
                                button_L1;;
                            5)
                                button_R1;;
                            6)
                                button_SELECT;;
                            7)
                                button_START;;
                            8)
                                button_HOME
                                ;;
                            9|10)
                                # press joysticks
                                ;;
                            *)
                                button_unknow "$action" "$button";;
                        esac;;
                esac;;
            2)
                case $button in
                    6)
                        case $value in
                            32767)
                                button_RIGHT;;
                            -32767)
                                button_LEFT;;
                        esac;;
                    7)
                        case $value in
                            32767)
                                button_DOWN;;
                            -32767)
                                button_UP;;
                        esac;;
                    0|1|3|4)
                        # joysticks
                        ;;
                    2)
                        case $value in
                            32767) # press
                                button_L2;;
                        esac;;
                    5)
                        case $value in
                            32767) # press
                                button_R2;;
                        esac;;
                    *)
                        button_unknow "$action" "$button";;
                esac;;
            0)
                #pull
                ;;
            *) 
                case $button in
                    0002|0102|0202|0302|0402)
                        # joysticks
                        ;;
                    *)
                        button_unknow "$action" "$button";;
                esac;;
        esac
    fi
}

parse_8BitDo_USB_data
