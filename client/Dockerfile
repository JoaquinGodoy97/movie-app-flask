# Use the official Node.js image
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile --production

# Copy app source
COPY . .

# Build the app
RUN yarn build

EXPOSE 3000

# Start the app
CMD ["yarn", "start"]

