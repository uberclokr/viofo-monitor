# Viofo Monitor

A Kivy-based Android application for monitoring Viofo dashcams via RTSP streaming and HTTP commands.

## Documentation

*   **[COMMANDS.md](COMMANDS.md)**: A list of implemented and potential future commands for the camera (DISCLAIMER:these have not all been tested. Info was retrieved from this [forum post](https://dashcamtalk.com/forum/threads/how-to-access-the-a129-over-wi-fi-without-the-viofo-app.37279/))
*   **[Survey3-WIFI-Manual.pdf](Survey3-WIFI-Manual.pdf)**: The original documentation for the HTTP RPC protocol used by this camera.

## TODO

- Khadas Edge 2 and Raspberry Pi GPIO support to detect vehicle reverse to automatically display the rear camera.
- Media browser to view recorded videos

## Features
- Low-latency RTSP streaming.
- 3-Camera View Switching (Front/Interior/Rear).
- Firmware Version display.
- One-click Reboot.

## Build

Built with [Buildozer](https://github.com/kivy/buildozer).

```bash
buildozer android debug
```
