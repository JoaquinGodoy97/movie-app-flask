# Use the official Node.js image
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package.json yarn.lock ./

# Add this line before `RUN yarn install`
ENV NODE_ENV=development

RUN yarn install --frozen-lockfile

# Copy app source
COPY . .

# Build the app
RUN yarn build

# Start the app
CMD ["yarn", "start"]

