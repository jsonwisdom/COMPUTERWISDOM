FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=4s --start-period=5s --retries=3 CMD wget -q -O - http://127.0.0.1:8080/ | grep -q "Citizen Audit Vortex" || exit 1
