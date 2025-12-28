from extensions import db
from models.result import Result
from models.user import User


class UserQueries:

    def add_user(self, new_user):
        try:
            print("================> adding new user")
            present_user = self.get_user_by_name(new_user.name).res

            if len(present_user) == 0:
                db.session.add(new_user)
                db.session.commit()

                result_status = Result(new_user, "success", f"User {new_user.name} successfully added", 200)
                print(result_status.message)
                print("================> finished adding new user")
                return result_status.get_message()

            else:
                print("================> finished adding new user")
                result_status = Result(new_user, "error", f"User {new_user.name} already exists", 403)
                print(result_status.message)
                return result_status.get_message()



        except Exception as e:
            result_status = Result("", "error", f"Error adding user: {e}", 500)
            print(result_status.message)
            return result_status.get_message()


    def get_user_by_name(self, name):
        try:
            print("=================> getting user by name")
            user = User.query.filter_by(name=name).all()

            if len(user) == 0:
                result_status = Result(user, "error", f"User {name} does not exist", 403)
                print(result_status.get_message())
                print("==================> finished getting user by name")
                return result_status

            else:

                print("==================> finished getting user by name")
                result_status = Result(user, "success", f"User {name} already exists in DB", 200)
                print(result_status.message)

                return result_status.get_message()



        except Exception as e:
            result_status = Result("", "error", f"Error getting user by name: {e}", 500)
            print(result_status.message)
            return result_status.get_message()