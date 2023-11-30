import http from "http";
import { handleFindProject } from "./requestHandlers/handleFindProject";
import { handleNewProject } from "./requestHandlers/handleNewProject";
import { handleNotFound } from "./requestHandlers/handleNotFound";
import { handleUpdateProject } from "./requestHandlers/handleUpdateProject";
import { getUrlFromRequest } from "./requestHandlers/helpers/getUrlFromRequest";

type RequestHandler = (
  req: http.IncomingMessage,
  res: http.ServerResponse
) => Promise<void>;

type RouteHandlers = {
  [method: string]:
    | {
        [route: string]: RequestHandler | undefined;
      }
    | undefined;
};

// Define which combination of methods and routes corrosponds to which functions
const routeHandlers: RouteHandlers = {
  GET: {
    "/projects": handleFindProject,
  },
  POST: {
    "/projects": handleNewProject,
  },
  PUT: {
    "/projects": handleUpdateProject,
  },
};

// Function that gets called for every request to the server
const requestHandler: RequestHandler = async (req, res) => {
  // Add cors headers to every response
  addCorsHeaders(res);

  // Find the approiate request handler
  const url = getUrlFromRequest(req);
  if (req.method !== undefined && url !== null) {
    const handlers = routeHandlers[req.method];
    const handler = handlers ? handlers[url.pathname] : undefined;

    if (handler !== undefined) {
      await handler(req, res);
    }
  }
  // No approiate request handler was found
  if (!res.writableEnded) {
    if (req.method === "OPTIONS") {
      // Only send the cors headers for all OPTIONS requests. This is necessary
      // for cors preflight:
      // https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
      res.writeHead(200);
      res.end();
    } else {
      handleNotFound(req, res);
    }
  }
};

// Create a http server on port 3280 that uses the request handler for incoming
// requests
const server = http.createServer(requestHandler);
server.listen(3280);

function addCorsHeaders(res: http.ServerResponse) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "*");
  res.setHeader("Access-Control-Max-Age", 2592000); // 30 days
}
