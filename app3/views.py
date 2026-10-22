from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from django.contrib import messages



def signin(request):
    return render(request, 'signin.html')



# def login(request):

#     print("LOGIN FUNCTION CALLED")
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         upass = request.POST.get('upass')

#         # Connect to the MySQL database
#         mydb = mysql.connector.connect(
#             host="127.0.0.1",
#             user="root",
#             password="",
#             database="disease"  # Replace with your database name
#         )

#         cursor = mydb.cursor()

#         try:
#             # Check if the user exists using email
#             cursor.execute("SELECT * FROM usermast WHERE email = %s", (email,))
#             user = cursor.fetchone()
#             print("User from DB:", user)
#             print("Entered Email:", email)
#             print("Entered Password:", upass)

#             # Ensure that no unread results exist by consuming them
#             cursor.fetchall()  # Explicitly consume any remaining results

#             if user:
#                 print("Database Password:", user[2])


#                 # If user exists, check the password
#                 if user[2] == upass:  # user[2] is the password (upass)
#                     # Create session for the user
#                     print("LOGIN SUCCESS")
#                     request.session['id'] = user[0]  # Storing user UID in session
#                     request.session['email'] = user[3]  # Storing email in session
#                     request.session['uname'] = user[1]  # Storing username in session
#                     return redirect('home')  # Redirect to home page after successful login
#                 else:
#                     messages.error(request, "Invalid password")
#             else:
#                 messages.error(request, "User does not exist")

#         except mysql.connector.Error as e:
#             messages.error(request, f"Database error: {str(e)}")
#         finally:
#             cursor.close()

#     return render(request, 'signin.html', {'user': request.user})
def login(request):
    print("LOGIN FUNCTION CALLED")

    if request.method == 'POST':
        email = request.POST.get('email')
        upass = request.POST.get('upass')

        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="disease"
        )

        cursor = mydb.cursor()

        try:
            cursor.execute("SELECT * FROM usermast WHERE email=%s", (email,))
            user = cursor.fetchone()

            print("User from DB:", user)

            if user:
                print("Database Password:", user[2])

                if str(user[2]).strip() == str(upass).strip():
                    print("LOGIN SUCCESS")

                    request.session['id'] = user[0]
                    request.session['uname'] = user[1]
                    request.session['email'] = user[3]

                    return redirect('home')   # <-- Redirect to home
                else:
                    messages.error(request, "Invalid password")
            else:
                messages.error(request, "User does not exist")

        except mysql.connector.Error as e:
            messages.error(request, f"Database error: {e}")

        finally:
            cursor.close()
            mydb.close()

    return render(request, "signin.html")

def logout_view(request):
    request.session.flush()  # Clear the session data
    return redirect('home')  # Redirect to home page aft