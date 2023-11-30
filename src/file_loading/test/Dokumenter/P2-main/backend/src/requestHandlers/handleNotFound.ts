import http from "http";

// Example:
// GET /invalid-route
// Response: GET /invalid-route not found
export function handleNotFound(
  req: http.IncomingMessage,
  res: http.ServerResponse
) {
  // Status code 404 for not found
  res.writeHead(404);

  // Write information to body about the request
  res.end(`${req.method} ${req.url} not found`);
}
