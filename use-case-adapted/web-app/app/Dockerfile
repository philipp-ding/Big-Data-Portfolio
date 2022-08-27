# Select base image https://hub.docker.com/_/node/
FROM node:alpine

# Expose port 8080
EXPOSE 8080

# Set working dir for consecutive commands
WORKDIR /src

# Add dependencies
ADD package.json package-lock.json /src/
RUN npm install

# Copy app source
ADD index.js /src/

# Set (default) command to execute on startup
CMD node /src/index.js