from public.router_authors import create_author

def test_create_author(session):
    # Подготовка данных для создания автора
    author_data = {"name": "Test Author", "birth_year": 1990}

    # Вызов функции создания автора с предварительно созданной сессией
    author = create_author(author_data, session=session)

    # Проверка, что автор создан корректно
    assert author.name == author_data["name"]
    assert author.birth_year == author_data["birth_year"]
    assert author.id is not None