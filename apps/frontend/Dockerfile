# Simple single-stage build for SvelteKit Frontend
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies needed for build)
ENV NODE_ENV=development
RUN npm install --verbose

# Copy source code
COPY . .

# Build the application (use full path to avoid PATH issues)
RUN /app/node_modules/.bin/vite build

# Copy health check script (if it doesn't exist, create a simple one)
RUN echo 'const http = require("http"); const options = { hostname: "localhost", port: 3000, path: "/", method: "GET" }; const req = http.request(options, (res) => { process.exit(res.statusCode === 200 ? 0 : 1); }); req.on("error", () => { process.exit(1); }); req.end();' > healthcheck.js

# Expose the application port
EXPOSE 3000

# Set environment variables for production
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0

# Add health check for container monitoring
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node healthcheck.js || exit 1

# Start the SvelteKit application
CMD ["node", "build/index.js"]