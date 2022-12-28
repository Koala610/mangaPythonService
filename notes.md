1. PYTHONUNBUFFERED=1 
2. (echo > /dev/tcp/"$1"/"$2") > /dev/null 2>&1
exit_code=$?    : более лучшая проверка статуса mysql сервера