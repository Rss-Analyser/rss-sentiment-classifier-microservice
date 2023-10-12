# rss-sentiment-classifier-microservice

A Flask-based microservice that classifies sentiments of RSS feeds. Built with Python, this service provides endpoints to initiate sentiment classification on RSS feed data and fetch the status of classification. The service utilizes an SQLite database for storage, which can be mounted from a network drive for flexibility and scalability. Docker support is included for easy deployment and scalability.

Features:

Flask-based REST API endpoints.
Integration with SQLite for data storage.
Dockerization for easy deployment.
Configurable settings via a YAML file.
Threaded sentiment classification for non-blocking operations.
Endpoints:


/classify_sentiment: Initiates the sentiment classification.

/status: Retrieves the status of the classification process.
