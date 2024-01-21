from lib.space_repository import SpaceRepository
from lib.space import Space


# test when called all spaces are returned
def test_get_all_spaces(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = SpaceRepository(db_connection)

    spaces = repository.get_all_spaces()
    assert spaces == [
        Space(
            1,
            "Enchanted Retreat",
            "Discover the magic of this hidden gem. A cozy haven surrounded by nature, perfect for a peaceful escape.",
            130,
            1,
        ),
        Space(
            2,
            "Urban Oasis Loft",
            "Experience city living at its finest. Our modern loft offers stunning views and all the amenities you need for a stylish stay.",
            130,
            2,
        ),
        Space(
            3,
            "Sunset Serenity Cottage",
            "Unwind in our charming cottage with breathtaking sunset views. A tranquil setting for a memorable getaway.",
            130,
            3,
        ),
        Space(
            4,
            "Luxury Skyline Penthouse",
            "Indulge in luxury high above the city. Our penthouse boasts panoramic skyline views and top-notch amenities.",
            130,
            4,
        ),
        Space(
            5,
            "Seaside Bliss Villa",
            "Escape to paradise in our seaside villa. Relax to the sound of waves and enjoy the ultimate beachfront experience.",
            130,
            1,
        ),
    ]


# test that a single space, with the corresponding info, is returned when called
# with a certain space id.
def test_get_space_by_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = SpaceRepository(db_connection)

    space3 = repository.get_space_by_id(3)
    assert space3 == Space(
        3,
        "Sunset Serenity Cottage",
        "Unwind in our charming cottage with breathtaking sunset views. A tranquil setting for a memorable getaway.",
        130,
        3,
    )


# Test a space is created in the database when called.
def test_add_space_to_db(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = SpaceRepository(db_connection)

    # id will be overwritten by corresponding database id
    space = Space(1, "Test Name", "Test Description", 50.5, 5)
    repository.add_space_to_db(space)
    assert repository.get_all_spaces() == [
        Space(
            1,
            "Enchanted Retreat",
            "Discover the magic of this hidden gem. A cozy haven surrounded by nature, perfect for a peaceful escape.",
            130,
            1,
        ),
        Space(
            2,
            "Urban Oasis Loft",
            "Experience city living at its finest. Our modern loft offers stunning views and all the amenities you need for a stylish stay.",
            130,
            2,
        ),
        Space(
            3,
            "Sunset Serenity Cottage",
            "Unwind in our charming cottage with breathtaking sunset views. A tranquil setting for a memorable getaway.",
            130,
            3,
        ),
        Space(
            4,
            "Luxury Skyline Penthouse",
            "Indulge in luxury high above the city. Our penthouse boasts panoramic skyline views and top-notch amenities.",
            130,
            4,
        ),
        Space(
            5,
            "Seaside Bliss Villa",
            "Escape to paradise in our seaside villa. Relax to the sound of waves and enjoy the ultimate beachfront experience.",
            130,
            1,
        ),
        Space(6, "Test Name", "Test Description", 50.5, 5),
    ]
