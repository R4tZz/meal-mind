# Dockerfile for SvelteKit Frontend (Production)
# Note: This expects the app to be pre-built locally with 'npm run build'

FROM node:20-alpine AS production

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev dependencies for build)
RUN npm ci && npm cache clean --force

# Build the application to generate .svelte-kit/output
RUN npm run build

# Copy built application output
COPY .svelte-kit/output .

# Copy health check script
COPY healthcheck.js .

# Create a non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S sveltekit -u 1001

# Change ownership of the app directory to the non-root user
RUN chown -R sveltekit:nodejs /app
USER sveltekit

# Expose the application port
EXPOSE 3000

# Set environment variables for production
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0

# Add health check for container monitoring
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1

# Start the SvelteKit application
CMD ["node", "server/index.js"]