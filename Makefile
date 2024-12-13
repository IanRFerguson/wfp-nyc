# Run helper scripts to rebuild analytics file + map
map:
	@if [ ! -z $(tolerance) ]; then		\
		export TOLERANCE=$tolerance;	\
	fi		
	@./rebuild_map.sh
	

# Run Docker container locally
dev:
	@if [ ! -z $(build) ]; then 		\
		docker compose up --build; 		\
	else								\
		docker compose up;				\
	fi


# Run Flask server locally
local:
	@python src/server.py