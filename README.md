### Reference
- Basic concepts: https://dev.to/github/whats-the-difference-between-a-github-action-and-a-workflow-2gba
- Python sript: https://github.com/GuillaumeFalourd/poc-github-actions/blob/main/.github/workflows/03-python-script-workflow.yml
- HTTPs triggers: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch

- HTTP basics: https://www.tutorialspoint.com/http/http_requests.htm
  - Abstraction stack is IP (Packets and routing) -> TCP ('Correct' streams or chunks of data (aka files?)) -> HTTP (Made for webbrowser<->server connection but now also used for other communication)
  - HTTP requests are basically a string of text following a certain format (aka protocol) and then transmitted via TCP.
  - HTTP requests seems to be built around "forms". But all the stuff with "form" in it's name is now also used for other stuff.
    - See: https://eloquentjavascript.net/18_http.html <- This article is great
  - HTTP requests consist of
    - Request line containing METHOD, URI, and HTTP version
      - IIUC the server can map any METHOD to any action. METHODs don't 'do' anything. It's just convention that certain methods trigger certain types of actions.
      - URI specifies "the resource upon which to act". It's bascally the URL without the ?name=value part (aka the Query String). Can also be * for the whole server or a path relative to the server where the request originated. But that's not relevant for us.
    - Optional header(s)
      - These are just random key-value-pairs whose keys are conventionally used and therefore *probably* understood by the receiver
    - Optional body
      - This can be any data in any format. These are the 2 conventionally used formats which can be specified in the header with key "Content-Type":
        - application/x-www-form-urlencoded
          - Data is encoded to look like the queryString (key=value&key2=value2).
          - This is the default and most commonly used.
        - multipart/form-data
          - Body can have several sections all with different headers and encodings. I often read "use this when your form has file uploads"
      - There are also more formats like "application/json", or plaintext. 
      - I think the urlencoded can transmit nested datastructures somehow but not sure.
      - When your url contains a queryString the query string will automatically be made part of the body of the HTTP request (True for POST, not true for GET. Not sure about other METHODS)
        - So do you have to use application/x-www-form-urlencoded when using a queryString?
        - Can you use a queryString and also send additional data? That would probably use `multipart/form-data`.

- TCP ports seem to be pretty unnecessary. I think ports were originally made to allow for simultaneous connection sessions, but there can be several connection sessions on a single TCP port. Port numbers are conventionally used for specific higher level protocols (e.g. port 80 for HTTP). But I feel like everything would work fine if ports didn't exist.
