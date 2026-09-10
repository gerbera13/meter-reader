echo "=== Проверка списка моделей ==="
curl -s http://127.0.0.1:1234/v1/models | python3 -m json.tool

echo ""
echo "=== Отправка тестового запроса (без картинки) ==="
curl -s http://127.0.0.1:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "PLACEHOLDER",
    "messages": [{"role": "user", "content": "Привет, скажи OK"}],
    "max_tokens": 5
  }'
