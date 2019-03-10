"""Helper functions that assist with testing, but are themselves not fixtures."""

def clear_data(db):
    """Clear all data in the database so the test suite has a clean slate to work with."""
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def verify_model(loaded_data, expected, model_type):
    """
    Check that each key of the expected result is the same as the returned data.

    Ignores passwords and ids.
    Recursively calls self on each object in wishlist.
    """
    for key in expected:
        if key == 'password' or key == 'wishlist':
            continue
        assert loaded_data[key] == expected[key]
    assert loaded_data['type'] == model_type
    if 'wishlist' in loaded_data:
        for i in range(len(expected['wishlist'])):
            verify_model(loaded_data['wishlist'][i], expected['wishlist'][i], 'book')
