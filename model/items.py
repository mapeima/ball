import logging

from model.DBConnection import DBCOnnection


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

connection = DBCOnnection()


def get_items(username, path=None):
    """Returns the items owned by the user in a selected path if this is passed, else returns all items.

    Args:
        username (str): The username of the user.
        path (str): The optional path where search the items.

    Returns:
        list: A list containing the items ordered by position.
    """
    query = "SELECT name FROM items WHERE username = '{}' ".format(username)

    if path:
        query += "AND path = '{}' ".format(path)

    query += "ORDER BY position"

    try:
        return connection.execute(query)

    except Exception as e:
        logger.error(e)

        raise e


def get_last_pos_for_path(username, path):
    """Returns the last position of the items in a selected path

    Args:
        username (str): The username of the user
        path (str): The path where to find the last position

    Returns:
        int: The last position of the items in a selected path
    """
    query = "SELECT MAX(position) as max FROM items WHERE username = '{}' AND path = '{}'".format(username, path)

    try:
        return connection.execute(query)[0]['max']

    except Exception as e:
        logger.error(e)

        raise e


def insert_items(username, path, items):
    """Insert the items in the selected path of the user.

    Args:
        username (str): The username of the user.
        path (str): The path where to insert the items.
        items (list): The items to be inserted in the database.
    """
    next_index = get_last_pos_for_path(username, path) + 1

    stmt = "INSERT INTO items VALUES('{}', '{}', ".format(username, path)

    try:
        for item in items:
            connection.execute(stmt + "'{}', {})".format(item, next_index))

    except Exception as e:
        logger.error(e)

        raise e
