#!/bin/bash
cd /home/Diego/API-test/log_backup_demo

# Cargar variables de entorno
source .env
API_URL="${API_BASE_URL}/backup"
RESTORE_URL="${API_BASE_URL}/restore"
HEADER="X-RapidAPI-Proxy-Secret: ${RAPIDAPI_KEY}"

echo "======================================================"
echo "1. GENERANDO UN ARCHIVO DE LOG FÍSICO REAL"
echo "======================================================"
rm -f real_server.log restored_real_server.log
# Generar un archivo de log de aproximadamente 1.5 MB para probar (para respetar el límite actual)
for i in {1..20000}; do
    echo "2026-04-10 10:00:00 [INFO] System heartbeat check $i - Memory OK, CPU 12%, Network stable." >> real_server.log
done
FILE_SIZE=$(ls -lh real_server.log | awk '{print $5}')
echo "✅ Creado 'real_server.log'. Tamaño: $FILE_SIZE"

echo -e "\n======================================================"
echo "2. PRIMER BACKUP (Versión 1)"
echo "======================================================"
curl -s -X POST -F "file=@real_server.log" -H "$HEADER" "$API_URL/real_log_v1" > result_v1.json
python3 -m json.tool result_v1.json

echo -e "\n======================================================"
echo "3. RESTAURANDO EL BACKUP (Versión 1)"
echo "======================================================"
curl -s -X GET -H "$HEADER" "$RESTORE_URL/real_log_v1" -o restored_real_server.log
RESTORED_SIZE=$(ls -lh restored_real_server.log | awk '{print $5}')
echo "✅ Archivo restaurado a 'restored_real_server.log'. Tamaño: $RESTORED_SIZE"

if cmp -s real_server.log restored_real_server.log; then
    echo "✅ Verificación: ¡El archivo restaurado es EXACTAMENTE igual al original!"
else
    echo "❌ Verificación: Los archivos son diferentes."
fi

echo -e "\n======================================================"
echo "4. AÑADIENDO NUEVOS LOGS AL MISMO ARCHIVO"
echo "======================================================"
echo "Simulando que el servidor siguió operando y generó nuevos errores..."
for i in {1..50}; do
    echo "2026-04-11 08:15:22 [ERROR] Database connection lost! Attempt $i" >> real_server.log
done
NEW_FILE_SIZE=$(ls -lh real_server.log | awk '{print $5}')
echo "✅ Archivo 'real_server.log' modificado. Nuevo tamaño: $NEW_FILE_SIZE"

echo -e "\n======================================================"
echo "5. SEGUNDO BACKUP (Versión 2 - Demostrando el ahorro)"
echo "======================================================"
curl -s -X POST -F "file=@real_server.log" -H "$HEADER" "$API_URL/real_log_v2" > result_v2.json
python3 -m json.tool result_v2.json

echo -e "\n======================================================"
echo "¡Mira 'chunks_dedup' en el segundo backup! 🤯"
echo "Casi todos los bloques fueron reutilizados, ahorrando megabytes enteros."
echo "======================================================"

