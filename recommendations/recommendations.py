# recommendation.py

from concurrent.futures import ThreadPoolExecutor

import random

import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse
)

import recommendations_pb2_grpc

# Создаем словарь "базы данных" - категории и книги
books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="Мальтийский сокол"),
        BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
        BookRecommendation(id=3, title="Собака Баскервилей"),
        BookRecommendation(id=4, title="Автостопом по галактике"),
        BookRecommendation(id=5, title="Тень над Иннсмутом"),
        BookRecommendation(id=6, title="Девушка с татуировкой дракона"),
        BookRecommendation(id=7, title="Идеальный шторм"),
        BookRecommendation(id=8, title="Молчание ягнят"),
        BookRecommendation(id=9, title="Последнее дело Холмса"),
        BookRecommendation(id=10, title="Тайна старого особняка"),


    ],

    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=11, title="Дюна"),
        BookRecommendation(id=12, title="Фонд"),
        BookRecommendation(id=13, title="Автостопом по Галактике"),
        BookRecommendation(id=14, title="Нейромант"),
        BookRecommendation(id=15, title="Игра Эндера"),
        BookRecommendation(id=16, title="Солярис"),
        BookRecommendation(id=17, title="Гиперион"),
        BookRecommendation(id=18, title="Левиафан пробуждается"),
        BookRecommendation(id=19, title="Парк Юрского периода"),
        BookRecommendation(id=20, title="Звёздный десант"),
    ],

    BookCategory.SELF_HELP: [
        BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
        BookRecommendation(id=22, title="Как завоёвывать друзей и оказывать влияние на людей"),
        BookRecommendation(id=23, title="Человек в поисках смысла"),
        BookRecommendation(id=24, title="Атомные привычки"),
        BookRecommendation(id=25, title="Магия утра"),
        BookRecommendation(id=26, title="Сила настоящего"),
        BookRecommendation(id=27, title="Богатый папа, бедный папа"),
        BookRecommendation(id=28, title="Гибкое сознание"),
        BookRecommendation(id=29, title="4-часовая рабочая неделя"),
        BookRecommendation(id=30, title="Привычка приносить пользу"),
    ],
}

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):

    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Категория не найдена")

        books_for_category =  books_by_category[request.category]

        num_result = min(request.max_result, len(books_for_category))

        books_to_recommend = random.sample(books_for_category, num_result)

        return RecommendationResponse(recommendations=books_to_recommend)


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))

    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)

    server.add_insecure_port('0.0.0.0:50051')
    server.start()

    print("Сервер запущен на порту 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()




