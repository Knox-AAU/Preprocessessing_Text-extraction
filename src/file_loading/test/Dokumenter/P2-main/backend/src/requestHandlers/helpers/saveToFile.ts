import { promises } from "fs";
import { createDirIfNotExist } from "./createDirIfNotExist";
export async function saveToFile<T>(path: string, object: T): Promise<void> {
  // Transform object to JSON string
  const jsonString = JSON.stringify(object);

  await createDirIfNotExist("./data");

  // Overwrite file at location with contents of JSON string
  await promises.writeFile(`./data/${path}`, jsonString);
}
