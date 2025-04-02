# openbb-widgets
Custom widgets I created to implement into the openbb workspace as backend widgets

# Screener Widget using fmp Installation Guide
![Screenshot 2025-04-02 011746](https://github.com/user-attachments/assets/c3dd61fa-af6f-4ed7-acc0-7d0fea8c56b5)


## Installation

## Prerequisites

make sure you have gone to openbb hub and entered your fmp api token or this will not work (fmp api tokens are free)

### Option 1: Run Locally (Recommended with Virtual Environment)

1. Download the `ScreenerWidget` folder.

2. Ensure you are running **Python 3.10** (other versions may not work and are untested).

3. Install dependencies:

   ```bash
   pip install openbb[all]
   ```

4. Run the application:

   ```bash
   uvicorn screener:app --host 0.0.0.0 --port 5050 --env-file .env
   ```

5. Make sure to enter your OpenBB PAT into the `.env` file.

### Option 2: Run in Docker with Cloudflare tunnels to a domain

1. Download the `ScreenerWidget` folder.

2. Create an image from the Dockerfile or pull from [bigdave223/openbbscreener:latest](https://hub.docker.com/r/bigdave223/openbbscreener)

3. Run the application using Docker Compose after entering your OpenBB PAT and Cloudflare tunnel token in the `.env`:

   ```bash
   docker compose up
   ```

4. If you don't want to use Cloudflare tunnels, then you just need to add:

   ```bash
   ports:
     - 5050:5050
   ```

   and it will map to your host computer `0.0.0.0:5050`. then remove the cloudflare service from the compose file.

## How to use

1. Add the URL of your instance into OpenBB under data connectors, backends.

2. Add the widget to a workspace, and you might have to click the three dots in the top right, then go to quick actions and select "Auto-size columns."
   
![Screenshot 2025-04-02 011807](https://github.com/user-attachments/assets/d40771ef-8b44-4bfd-8712-da53e893c426)

4. The screener is highly customizable, and you can filter with the parameters at the top.

Let me know if there are any changes I should make as I am newer to Python, JSON, and OpenBB.

Thanks to the OpenBB team for a wonderful platform. I have enjoyed this project and am definitely going to be working on more.
