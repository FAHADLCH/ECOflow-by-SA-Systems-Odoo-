# ECOFLOW local dev helpers.
# Override Odoo version: make up TAG=19   (supported: 18, 19)

TAG ?= 18
DB  ?= ecoflow
MODULES ?= ecoflow

export ODOO_TAG = $(TAG)

.PHONY: up down logs restart init update shell psql clean

up:            ## Start the stack (Odoo + Postgres)
	ODOO_TAG=$(TAG) docker compose up -d
	@echo "ECOFLOW is starting on http://localhost:8070  (Odoo $(TAG))"

down:          ## Stop the stack
	docker compose down

logs:          ## Tail Odoo logs
	docker compose logs -f odoo

restart:       ## Restart Odoo
	docker compose restart odoo

init:          ## Create DB '$(DB)' and install all ECOFLOW modules (with demo data)
	docker compose run --rm odoo odoo \
		--config=/etc/odoo/odoo.conf \
		-d $(DB) -i $(MODULES) --stop-after-init
	@echo "Initialized. Now run: make up  -> http://localhost:8070"

update:        ## Upgrade all ECOFLOW modules in DB '$(DB)'
	docker compose run --rm odoo odoo \
		--config=/etc/odoo/odoo.conf \
		-d $(DB) -u $(MODULES) --stop-after-init

shell:         ## Open an Odoo shell on DB '$(DB)'
	docker compose run --rm odoo odoo shell \
		--config=/etc/odoo/odoo.conf -d $(DB)

psql:          ## Open psql on the database container
	docker compose exec db psql -U odoo -d $(DB)

clean:         ## Stop and DELETE all data volumes (destructive)
	docker compose down -v
