PYTHON ?= python3
.PHONY: help demo secure check report install-dissector
help:
	@echo "make demo               - коротке TCP/TLS-демо з меню"
	@echo "make secure             - локальний HTTP-приклад через TLS"
	@echo "make check              - перевірка файлів без мережевих дій"
	@echo "make report             - PDF із defender-report.md"
	@echo "make install-dissector  - встановити Lua для Wireshark"
demo:
	$(PYTHON) wired_lab/traffic.py
secure:
	printf '1\n1\n' | $(PYTHON) wired_lab/traffic.py
check:
	$(PYTHON) scripts/check_project.py
report:
	$(PYTHON) scripts/build_report.py
install-dissector:
	install -Dm644 tools/wireshark/mavlink_common.lua "$(HOME)/.local/lib/wireshark/plugins/mavlink_common.lua"
