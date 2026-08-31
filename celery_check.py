from app.workers.tasks import test_task

result = test_task.delay("Tilak")

print(result.id)

print(result.get(timeout=10))