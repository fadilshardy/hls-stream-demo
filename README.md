# CCTV Streaming Server

## Overview

Docker app for streaming `.mp4` videos via HLS.

## Components

- **Frontend**: Svelte app for video playback.
- **API**: Flask backend for HLS generation.
- **Nginx**: Serves HLS files and routes requests.

## Setup

1. Put `.mp4` files in the `shared/` folder.
2. Run with `docker-compose up --build`.
3. Open `http://localhost:5001`.

## Folders

- `shared/`: Input videos.
- `hls-output/`: HLS files.

```
cctv-server
├─ docker-compose.yml
├─ hls-api
│  ├─ app.py
│  ├─ Dockerfile
│  └─ requirements.txt
├─ hls-output
│  ├─ output.m3u8
├─ shared
│  └─ jakarta-drive-1080p.mp4
└─ svelte-app
   ├─ Dockerfile
   ├─ package-lock.json
   ├─ package.json
   ├─ public
   │  ├─ favicon.png
   │  ├─ global.css
   │  └─ index.html
   ├─ README.md
   ├─ rollup.config.js
   ├─ scripts
   │  └─ setupTypeScript.js
   ├─ src
   │  ├─ app.css
   │  ├─ App.svelte
   │  └─ main.js
   └─ tailwind.config.js
```
