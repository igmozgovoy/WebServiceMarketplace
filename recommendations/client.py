import grpc

from recommendations_pb2 import (
    BookCategory,
    RecommendationRequest,
)

import recommendations_pb2_grpc

channel = grpc.insecure_channel("127.0.0.1:50051")

client = recommendations_pb2_grpc.RecommendationsStub(channel)

request = RecommendationRequest(
    user_id=1,
    category=BookCategory.SCIENCE_FICTION,
    max_result=3
)

response = client.Recommend(request)

print("Получено рекомендаций:", len(response.recommendations))
for book in response.recommendations:
    print(f"- {book.id}: {book.title}")

