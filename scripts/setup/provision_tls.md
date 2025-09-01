TLS (Let's Encrypt webroot) provisioning steps:

1) Set your domain in infrastructure/docker/nginx/nginx.conf under server_name.
2) Ensure ports 80/443 are open to the internet.
3) Start Nginx (HTTP only is fine initially):
   docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d nginx
4) Issue certs inside a certbot container (webroot):
   docker run --rm -v $(pwd)/infrastructure/docker/nginx/ssl:/etc/letsencrypt -v $(pwd)/infrastructure/docker/nginx/certbot:/var/www/certbot certbot/certbot certonly --webroot -w /var/www/certbot -d your.domain --email you@example.com --agree-tos --non-interactive
5) Restart full stack (Nginx will pick up /etc/nginx/ssl):
   docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d
6) Renewals run via the certbot service every ~12h; ensure volumes persist.


