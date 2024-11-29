# gpu-booking-app

This is a simple GPU booking app to manage the use of DGX Workstation server together easily.

## Quickstart

### Local Setup

1. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

2. Run the application:

    ```sh
    python main.py
    ```

3. Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Docker Setup

1. Build the Docker image:

    ```sh
    docker build -t gpu-booking-app .
    ```

2. Run the Docker container:

    ```sh
    docker run -p 5000:5000 gpu-booking-app
    ```

3. Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)