# API Usage Guide

This document provides instructions on how to use the Awesome-Project API.

## Authentication
All API requests must be authenticated. You must include your API key in the `Authorization` header of your request.

Example: `Authorization: Bearer YOUR_API_KEY`

## Rate Limits
To ensure fair usage, our API has a rate limit. You can make up to 100 requests per minute from a single IP address. If you exceed this limit, you will receive a `429 Too Many Requests` response.