import http from "http";

export function getUrlFromRequest(req: http.IncomingMessage): URL | null {
  return req.url !== undefined && req.headers.host !== undefined
    ? new URL(req.url, `http://${req.headers.host}`)
    : null;
}
