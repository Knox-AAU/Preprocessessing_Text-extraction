import http from "http";

export function consumeBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    // The resulting body
    let body = "";

    // Read every chunk of data from the request and add it to the body
    req.on("readable", () => {
      const chunk = req.read();
      if (chunk !== null) {
        body += chunk;
      }
    });

    // Resolve the promise with the body, when all the data has been read
    req.on("end", () => {
      resolve(body);
    });

    // Reject the promise if an error happens
    req.on("error", reject);
  });
}
