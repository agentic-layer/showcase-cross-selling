# Stage 1: Build React frontend
FROM node:22-alpine3.22 AS frontend-builder
WORKDIR /app/
COPY package*.json ./
RUN npm ci
COPY / ./
RUN npm run build

# Use nginx alpine image for lightweight static serving
FROM nginx:1.28-alpine3.21

# Install gettext for envsubst command
RUN apk add --no-cache gettext

# Remove default nginx configuration
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy nginx configuration template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Copy static frontend files from previous stage
COPY --from=frontend-builder /app/dist /usr/share/nginx/html/

# Set environment variables with defaults
ENV NGINX_PORT=80
ENV FRAME_OPTIONS=ALLOWALL

# Expose port
EXPOSE 80

# The base nginx image already has an entrypoint that will process our template
CMD ["nginx", "-g", "daemon off;"]
