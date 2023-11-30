import { existsSync, promises } from "fs";

export async function readFromFile<T>(
  path: string,
  validator: (object: unknown) => object is T
): Promise<T | null> {
  const fullPath = `./data/${path}`;

  // Check if file exists
  if (existsSync(fullPath)) {
    // Get file contents as string
    const fileString = (await promises.readFile(fullPath)).toString("utf8");

    // Parse the file contents as an object
    const fileObject: unknown = JSON.parse(fileString);

    if (validator(fileObject)) {
      // Return contents of file as an object representation
      return fileObject;
    } else {
      throw "File does not match type";
    }
  } else {
    // Return if file doesn't exist
    return null;
  }
}
