# P2 Project

## Get started

Start by installing the dependencies:

```bash
yarn && cd frontend && yarn && cd ../backend && yarn && cd ..
```

To run the frontend:

```bash
cd frontend
yarn dev
```

To run the backend:

```bash
cd backend
yarn dev
```

## Formatting code

To format the code, run the following in the root of the project (**WARNING: Remember to save your files before doing this command**):

```bash
yarn format
```

The formatting of the project will be checked when committing new changes to the repository. If you can't commit changes, try doing it through this command to see the error:

```bash
git commit -m "title"
```

## Setting up the editor

Install the following extensions:

- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)

Go to `settings.json` (Ctrl + shift + p -> Choose "Preferences: Open settings (JSON)") and paste the following:

```json
{
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.formatOnSave": true
}
```
