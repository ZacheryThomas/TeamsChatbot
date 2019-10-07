# TeamsChatbot

I designed this bot to be hosted in AWS Lambda. In order to make deployment and function management easier, I use [Serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/).

## Install Serverless Python Requirements
Serverless allows you to bundle up and send libraries found in your `requirements.txt` to your lambda functions. To do this we have to install a node package called `serverless-python-requirements`. Fortunately thats already in our `package.json` file so we can just npm install it.
```bash
npm i
```

## Deploying
```bash
sls deploy
```
