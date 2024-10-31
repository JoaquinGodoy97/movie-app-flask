# Use the official Node.js image
FROM node:14-alpine

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package.json yarn.lock ./
RUN yarn install

# Copy app source
COPY . .

# Build the app
RUN yarn build

# Start the app
CMD ["yarn", "start"]
