# Google Sheets

### Getting Started
#### Create an API key
1. goto https://console.cloud.google.com/welcome
2. new project
  - project_id is going the hostname of your email
3. goto https://console.cloud.google.com/apis/dashboard
4. create credentials
5. credentials > service account
  - your can add the permission later
6. keys > add key > create new key > json > create
  - convert to base64 - `cat <path-to-key.json> | base64`
7. copy .env.template into .env
8. Save the key as .env in the root of the project



