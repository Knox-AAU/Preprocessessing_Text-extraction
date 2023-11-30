import http from "http";

export function handleBadRequest(res: http.ServerResponse, message?: string) {
  // Status code 400 for Bad Request
  res.writeHead(400);
  res.end(message);
}
