import { existsSync, promises } from "fs";

export async function createDirIfNotExist(path: string) {
  if (!existsSync(path)) {
    // Create directory if it does not already exist
    await promises.mkdir(path);
  }
}
