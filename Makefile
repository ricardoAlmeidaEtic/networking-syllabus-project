up:
	docker compose up -d --build --force-recreate


tcp-client:
	docker compose run --rm tcp-client src/client/tcp.py



udp-client:
	docker compose run --rm udp-client src/client/udp.py