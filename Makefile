map:
	@echo "Rebuilding Folium map..."
	@./rebuild_map.sh
	
dev:
	@if [ ! -z $(build) ]; then 	\
		docker compose up --build; 	\
	fi
	@docker compose up