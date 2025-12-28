# Viofo Command Reference

Comprehensive list of HTTP RPC commands derived from [command_descriptors.java](file:///home/phill/Documents/Development/blugnu/viofo/command_descriptors.java).
Commands are sent via: `http://192.168.1.254/?custom=1&cmd=<ID>`

## Control Commands
| ID | Name | Description |
| :--- | :--- | :--- |
| **3028** | `PIP_STYLE` | Cycle Camera Views (Front/Rear/Pip) |
| **2001** | `MOVIE_RECORD` | Toggle Video Recording |
| **1001** | `PHOTO_CAPTURE` | Take Photo |
| **3001** | `CHANGE_MODE` | Switch Mode (Video/Photo/Playback) |
| **3018** | `RECONNECT_WIFI` | Reconnect Wi-Fi |
| **2020** | `REMOTE_CONTROL_FUNCTION` | Remote Control Function |
| **8200** | `POWER_ON_OFF_SOUND` | Power Sound |
| **9095** | `RESTART_CAMERA` | Restart Camera |
| **9423** | `RESTART_CAMERA` (Alt) | Restart Camera (A129) |

## Settings
| ID | Name | Description |
| :--- | :--- | :--- |
| **2002** | `MOVIE_REC_SIZE` | Recording Resolution |
| **2013** | `MOVIE_REC_BITRATE` | Recording Bitrate |
| **2003** | `MOVIE_CYCLIC_REC` | Loop Recording Interval |
| **2004** | `MOVIE_WDR` | Wide Dynamic Range |
| **2005** | `MOVIE_EV` | Exposure Value (Front?) |
| **9217** | `MOVIE_EV_REAR` | Exposure Value (Rear) |
| **2006** | `MOTION_DET` | Motion Detection |
| **2007** | `MOVIE_AUDIO` | Audio Recording |
| **2008** | `MOVIE_DATE_PRINT` | Date Stamp |
| **2009** | `MOVIE_MAX_RECORD_TIME` | Max Record Time |
| **2011** | `MOVIE_GSENSOR_SENS` | G-Sensor Sensitivity |
| **2012** | `MOVIE_AUTO_RECORDING` | Auto Recording |
| **2014** | `LIVE_VIEW_BITRATE` | Live View Bitrate |
| **2015** | `MOVIE_LIVE_VIEW_CONTROL` | Live View Control |
| **2016** | `MOVIE_RECORDING_TIME` | Recording Time |
| **2019** | `LIVE_VIEW_URL` | Check Live View URL |
| **1002** | `CAPTURE_SIZE` | Photo Size |
| **1003** | `PHOTO_AVAIL_NUM` | Photos Available |
| **3005** | `SET_DATE` | Set Date |
| **3006** | `SET_TIME` | Set Time |
| **3007** | `AUTO_POWER_OFF` | Auto Power Off |
| **3008** | `LANGUAGE` | System Language |
| **3009** | `TV_FORMAT` | TV Format (NTSC/PAL) |
| **3033** | `SET_NETWORK_MODE` | Set Network Mode |
| **9421** | `PARKING_MODE` | Parking Mode |
| **9412** | `SPEED_UNIT` | Speed Unit (KMH/MPH) |
| **9411** | `TIME_ZONE` | Time Zone |
| **9410** | `GPS` | GPS On/Off |
| **9405** | `SCREEN_SAVER` | Screen Saver |
| **9406** | `FREQUENCY` | Frequency (50Hz/60Hz) |
| **9403** | `BEEP` | Beep Sound (A129) |
| **9094** | `BEEP` | Beep Sound |
| **9093** | `IMAGE_ROTATE` | Image Rotate |
| **9413** | `IMAGE_ROTATE` (Alt) | Image Rotate (A129) |
| **9219** | `REAR_CAMERA_MIRROR` | Rear Camera Mirror |

## System Info & Maintenance
> [!WARNING]
> Use caution with formatting and reset commands.

| ID | Name | Description |
| :--- | :--- | :--- |
| **3012** | `FIRMWARE_VERSION` | Get Firmware Version |
| **3014** | `GET_CURRENT_STATE` | Get Current State |
| **3015** | `GET_FILE_LIST` | Get File List |
| **3016** | `HEART_BEAT` | Heartbeat |
| **3017** | `CARD_FREE_SPACE` | Check SD Card Free Space |
| **3024** | `GET_CARD_STATUS` | Get Card Status |
| **3019** | `GET_BATTERY_LEVEL` | Get Battery Level |
| **3026** | `GET_UPDATE_FW_PATH` | Get Firmware Update Path |
| **3003** | `WIFI_NAME` | Get/Set WiFi SSID |
| **3004** | `WIFI_PWD` | Get/Set WiFi Password |
| **3029** | `GET_WIFI_SSID_PASSWORD` | Get WiFi SSID & Password |
| **3025** | `FS_UNKNOW_FORMAT` | Filesystem Unknown |
| **3010** | `FORMAT_MEMORY` | Format SD Card |
| **3011** | `RESET_SETTING` | Factory Reset |
| **3023** | `REMOVE_LAST_USER` | Remove Last User |
| **4003** | `DELETE_ONE_FILE` | Delete Single File |
| **4004** | `DELETE_ALL_FILE` | Delete All Files |
| **4001** | `THUMB` | Get Thumbnail |
| **4002** | `SCREEN` | Screen Control? |

## Meta / Hardcoded
*   `A129_FIRMWARE_FILE_NAME`: `FWA129.bin`
*   `DEFAULT_IP`: `192.168.1.254`
*   `DEFAULT_PORT`: `3333` (Though probe failed on this port)
*   `STREAM_VIDEO`: `rtsp://192.168.1.254`
*   `STREAM_MJPEG`: `http://192.168.1.254:8192`
