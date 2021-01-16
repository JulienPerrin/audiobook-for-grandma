#!/bin/bash

source ./config.sh

stop_reader ()  {
    sudo kill $(ps -ef | grep audiobook | grep python | grep -v "grep" | awk '{ print $2 }')
    sudo kill $(ps -ef | grep mbrola | grep -v "grep" | awk '{ print $2 }')
    sudo kill $(ps -ef | grep aplay | grep -v "grep" | awk '{ print $2 }')
    echo "reader stopped reading"
    audiobook-for-grandma --stop 
}

button_A ()  {
    echo A
    stop_reader
}

button_B ()  {
    echo "B: audiobook-for-grandma --start --language $LANGUAGE --rate $RATE --volume $VOLUME --voice $VOICE >> log/start.log &"
    audiobook-for-grandma --start --language fr --rate $RATE --volume $VOLUME --voice $VOICE >> log/start.log &
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
        #echo "$USB_8BITDO_FILE exists."
        usb_data=$(hexdump -e '8/2 "%04x " "\n"' -s 144 -n 16 $USB_8BITDO_FILE)
        #echo $usb_data

        #press 'A'
        #e238 1f2f 0000 0782 ea12 1f2f 0001 0101
        regex='([[:alnum:]]{4}) ([[:alnum:]]{4}) ([[:alnum:]]{4}) ([[:alnum:]]{4}) ([[:alnum:]]{4}) ([[:alnum:]]{4}) ([[:alnum:]]{4}) ([[:alnum:]]{4})'
        if [[ $usb_data =~ $regex ]]; then
            action="${BASH_REMATCH[7]}"
            button="${BASH_REMATCH[8]}"
            #echo $action
            #echo $button
            case $action in
                0001)
                    #push
                    case $button in
                        0001)
                            button_B;;
                        0101)
                            button_A;;
                        0201)
                            button_Y;;
                        0301)
                            button_X;;
                        0401)
                            button_L1;;
                        0501)
                            button_R1;;
                        0701)
                            button_START;;
                        0601)
                            button_SELECT;;
                        0801)
                            button_HOME
                            ;;
                        *)
                            button_unknow $action $button;;
                    esac;;
                7fff)
                    case $button in
                        0602)
                            button_RIGHT;;
                        0702)
                            button_DOWN;;
                        0202)
                            button_L2;;
                        0502)
                            button_R2;;
                        0002|0102|0302|0402)
                            # joysticks
                            ;;
                        *)
                            button_unknow $action $button;;
                    esac;;
                8001)
                    case $button in
                        0202|0502)
                            #pull L2 R2
                            ;;
                        0602)
                            button_LEFT;;
                        0702)
                            button_UP;;
                        0002|0102|0302|0402)
                            # joysticks
                            ;;
                        *)
                            button_unknow $action $button;;
                    esac;;
                0000)
                    #pull
                    ;;
                *) 
                    case $button in
                        0002|0102|0202|0302|0402)
                            # joysticks
                            ;;
                        *)
                            button_unknow $action $button;;
                    esac;;
            esac
        fi
    else
        #echo "The file $USB_8BITDO_FILE does not exists (device not connected). "
        sleep 1
    fi
}

while true
do
    parse_8BitDo_USB_data
done

