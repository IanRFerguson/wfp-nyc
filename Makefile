# Run helper scripts to rebuild analytics file + map
map:
	@./rebuild_map.sh
	

# Run Docker container locally
dev:
	@if [ ! -z $(build) ]; then 	\
		docker compose up --build; 	\
	fi
	@docker compose up


# Run Flask server locally
local:
	@python src/server.py