# weather-tweet-api

## Description

This is a FastAPI server that provides weather information for cities and allows tweeting the weather updates.

## Prerequisites

Before running the server, make sure you have the following dependencies installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Python3+
- OpenWeatherMap API
- Twitter develop account

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/Deangelogn/weather-tweet-api.git
   ```
2. Navigate to the project directory:

   ```shell
   cd weather-tweet-api
   ```
3. Create a `.env` file in the project root directory and specify the required environment variables:weather-tweet-api

   ```
   WEATHER_API_KEY=<your_weather_api_key>
   CONSUMER_KEY=<your_twitter_consumer_key>
   CONSUMER_SECRET=<your_twitter_consumer_secret>
   ```

   Replace `<your_weather_api_key>`, `<your_twitter_consumer_key>`, and `<your_twitter_consumer_secret>` with your actual API keys and secrets.
4. Build the Docker image:

   ```shell
   docker build -t weather-tweet-api .
   ```
5. Run the Docker container:

   ```shell
   docker run -d -p 8000:8000 --env-file .env weather-tweet-api
   ```
6. The FastAPI server is now running inside the Docker container. You can access the API by visiting `http://localhost:8000` in your web browser or sending requests to it using tools like cURL or Postman.

## API Documentation

To view the API documentation and test the available endpoints, open your web browser and visit `http://localhost:8000/docs`. This will provide an interactive documentation interface powered by Swagger UI.

## Notes

- The server runs on port 8000 by default. If you need to use a different port, make sure to update the `-p` flag in the `docker run` command accordingly.
- Ensure that the necessary environment variables are correctly set in the `.env` file before running the Docker container.
- If you need to make changes to the code or configuration, you can edit the files in the project directory and rebuild the Docker image using the `docker build` command.
- To stop the server, use the `docker stop` command followed by the container ID or name.
- For production deployment, consider using appropriate security measures and configurations to protect sensitive information and ensure scalability and reliability.

## Usage

To tweet the weather in your Twitter account, follow these steps:

1. Authorize the application:
   * Access the `/gen-PIN` endpoint: `http://localhost:8000/gen-PIN`
   * You will be redirected to the authorization page of Twitter.
   * Authorize the application to post tweets on your behalf.
   * Twitter will provide you with a PIN number.
2. Tweet the weather:
   * Call the `/tweet-weather` endpoint using a tool like cURL or Postman.
   * Pass the following parameters in the request body:

     * `city`: The name of the city for which you want to tweet the weather.
     * `pin`: The PIN number obtained from the previous step.
   * Example cURL command:

     ```shell
     curl -X POST -H "Content-Type: application/json" -d '{"city": "New York", "pin": "
     ```

     Replace `<your_pin_number>` with the actual PIN number obtained from the authorization page.
3. If everything goes well, the weather for the specified city will be posted in your Twitter account as a tweet.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

```

Feel free to customize the README file based on your specific project details, including a more detailed description, installation instructions, and any other relevant information.
```
