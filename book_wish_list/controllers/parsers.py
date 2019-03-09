from flask_restplus import reqparse, fields


create_parser = reqparse.RequestParser()
create_parser.add_argument('first_name', type=str)
create_parser.add_argument('last_name', type=str)
create_parser.add_argument('email', type=str)
create_parser.add_argument('password', type=str)

update_parser = reqparse.RequestParser()
update_parser.add_argument('new_first_name', type=str)
update_parser.add_argument('new_last_name', type=str)
update_parser.add_argument('new_password', type=str)
update_parser.add_argument('new_email', type=str)
update_parser.add_argument('password', type=str)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('password', type=str)


wishlist_parser = reqparse.RequestParser()
wishlist_parser.add_argument('title', type=str)
wishlist_parser.add_argument('author', type=str)
wishlist_parser.add_argument('isbn', type=str)
wishlist_parser.add_argument('date_of_publication', type=fields.DateTime(dt_format='rfc822'), help='example: 2002-10-02')
wishlist_parser.add_argument('password', type=str)