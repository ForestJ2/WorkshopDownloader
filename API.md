# Paths & API

This document outlines the paths the webserver creates, and information about the API.

## Web Paths

These paths are typically interacted with by the user directly.

### Index Page

Paths:
- `/`
- `/index`

Returns the HTML file /templates/index.html to the client.

### Download Page

Path: `/archive/{workshop content id}`

Request Example: `GET http://localhost:5000/archive/7864237`

Returns a ZIP compressed archive of the content if it exists, otherwise a 404 status code and page.

## API Paths & Responses

These paths are requested by the browser, but indirectly by the user.

### Obtain content information from community workshop.

The server makes a request to a steamwork shop page and grabs the needed information to download the content. Th information is also used to update the UI to show the user progress.

Path: `/info/{id}`

Parameters:
- id: ID belonging to the workshop content.

Request Example: `GET http://localhost:5000/info/7864237`

Returns:
- JSON structure
- `error` bool in JSON to dictate result status
  - If `error` is true, it will be the only thing in the object.
- `game` and `content` objects each containing an `id` int, and `name` string.

Example Response:

```json
{
    "game": {
        "id": 4578439,
        "name": "This is a game"
    },

    "content": {
        "id": 7864237,
        "name": "Awesome content"
    },

    "error": false
}
```

### Request download

This is used to request the server download and compress workshop content.
This request is blocking, and finishes when the server finishes downloading the content, or runs into an error.

Most content size limits for steam workshop is 100MB, so there is no server side timeout currently. This is may change in the future.

Path: `/request/{game id}/{content id}`

Parameters:
- game id: ID of the game the workshop content belongs to.
- content id: ID of the workshop content.

Request Example: `GET http://localhost:5000/request/4578439/7864237`

Returns:
- JSON Structure
- `error` bool in JSON to dictate result status
- `url` string containing path to download the archive

Example Response:

```json
{
    "error": false,
    "url": "/archive/7864237"
}
```