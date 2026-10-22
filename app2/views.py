from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

# Create your views here.
def signup(request):
    return render(request, 'signup.html')

# def register(request):
#     # Get form data
#     print("function is called")
#
#     # s1 = request.GET.get("uname")
#     # s2 = request.GET.get("upass")
#     # s3 = request.GET.get("email")
#     # s4 = request.GET.get("mobile")
#
#     s1 = request.POST.get("uname")
#     s2 = request.POST.get("upass")
#     s3 = request.POST.get("email")
#     s4 = request.POST.get("mobile")
#
#     print("uname:", s1)
#     print("upass:", s2)
#     print("email:", s3)
#     print("mobile:", s4)
#     return render(request, "signin.html")
#
#     try:
#         # Connect to MySQL
#         mydb = mysql.connector.connect(
#             host="127.0.0.1",  # Use localhost for XAMPP
#             user="root",  # Default XAMPP user
#             password="",  # Leave blank if no password
#             database="disease"
#         )
#
#         cursor = mydb.cursor()
#
#         # Insert query
#         query = "INSERT INTO usermast (uname, upass, email, mobile) VALUES (%s, %s, %s, %s)"
#         values = (s1, s2, s3, s4)
#         cursor.execute(query, values)
#         mydb.commit()
#
#         # Close connection
#         cursor.close()
#         mydb.close()
#
#         return render(request,"signin.html")
#
#     except mysql.connector.Error as err:
#         return HttpResponse(f"Database error: {err}")
#
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {e}")
def register(request):

    print("function is called")

    if request.method == "POST":

        s1 = request.POST.get("uname")
        s2 = request.POST.get("upass")
        s3 = request.POST.get("email")
        s4 = request.POST.get("mobile")

        print("uname:", s1)
        print("upass:", s2)
        print("email:", s3)
        print("mobile:", s4)

        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="disease"
            )

            cursor = mydb.cursor()

            query = """
            INSERT INTO usermast (uname, upass, email, mobile)
            VALUES (%s, %s, %s, %s)
            """

            values = (s1, s2, s3, s4)

            cursor.execute(query, values)

            mydb.commit()

            print("Data inserted successfully")

            cursor.close()
            mydb.close()

            return render(request, "signin.html")

        except mysql.connector.Error as err:
            print(err)
            return HttpResponse(f"Database error: {err}")

    return render(request, "signup.html")
