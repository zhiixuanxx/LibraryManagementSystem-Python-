import time
from idlelib.run import exit_now
from operator import index
import datetime
import csv
import re


admin_username = 'AD1234'
admin_password = 'ad1234'
member_usn_list = []
member_pswd_list = []
member_name_list = []
librarian_usn_list = []
librarian_pswd_list = []
librarian_name_list = []
book_isbn_list= []
book_title_list= []
book_author_list= []
overdue_book_list= []
book_loan_list=[]
loan_date_list=[]
due_date_list=[]
return_date_list=[]
book_list=[]
book_status = 'Available'
book_status_list = []
member_usn_temp = []
member_usn_temp_list = []

def resetMemberList():
    member_usn_list.clear()
    member_pswd_list.clear()
    member_name_list.clear()

    with open('member.txt', 'r+') as file:
        lines = file.readlines()
        for line in lines:
            items = line.strip().split(',')

            member_usn = items[0].split(": ")[1].strip()
            member_pwd = items[1].split(": ")[1].strip()
            member_name = items[2].split(": ")[1].strip()

            member_usn_list.append(member_usn)
            member_pswd_list.append(member_pwd)
            member_name_list.append(member_name)

def resetLibrarianlist():
    librarian_usn_list.clear()
    librarian_pswd_list.clear()
    librarian_name_list.clear()

    with open('librarian.txt', 'r+') as file:
        lines = file.readlines()
        for line in lines:
            items = line.strip().split(',')

            librarian_usn = items[0].split(": ")[1].strip()
            librarian_pswd = items[1].split(": ")[1].strip()
            librarian_name = items[2].split(": ")[1].strip()

            librarian_usn_list.append(librarian_usn)
            librarian_pswd_list.append(librarian_pswd)
            librarian_name_list.append(librarian_name)

def resetBookList():
    book_isbn_list.clear()
    book_title_list.clear()
    book_author_list.clear()
    book_status_list.clear()

    with open('books.txt', 'r+') as file:
        lines = file.readlines()
        for line in lines:
            items = line.strip().split(',')

            book_isbn = items[0].split(": ")[1].strip()
            book_title = items[1].split(": ")[1].strip()
            book_author = items[2].split(": ")[1].strip()
            book_status = items[3].split(": ")[1].strip()

            book_isbn_list.append(book_isbn)
            book_title_list.append(book_title)
            book_author_list.append(book_author)
            book_status_list.append(book_status)

def resetBookLoanList():
    global book_loan_list
    book_loan_list = []
    with open('book_loans.txt', 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                member_id, book_isbn, loan_date, due_date = line.strip().split('|')
                loan = {
                    'member_id': member_id,
                    'book_isbn': book_isbn,
                    'loan_date': datetime.datetime.strptime(loan_date, '%Y-%m-%d').date(),
                    'due_date': datetime.datetime.strptime(due_date, '%Y-%m-%d').date(),
                    'return_date': None
                }
                book_loan_list.append(loan)

def xor_encrypt(data: str, key= 'secret') -> str: #encrypt password
    data_bytes = data.encode()
    key_bytes = key.encode()
    extended_key = key_bytes * (len(data_bytes) // len(key_bytes) + 1)
    extended_key = extended_key[:len(data_bytes)]
    # Perform XOR
    encrypted_bytes = bytes(a ^ b for a, b in zip(data_bytes, extended_key))
    # Return as hex string for readable output
    return encrypted_bytes.hex()

def xor_decrypt(encrypted_hex: str, key= 'secret') -> str: #decrypt password
    encrypted_bytes = bytes.fromhex(encrypted_hex)
    key_bytes = key.encode()
    extended_key = key_bytes * (len(encrypted_bytes) // len(key_bytes) + 1)
    extended_key = extended_key[:len(encrypted_bytes)]
    # XOR
    decrypted_bytes = bytes(a ^ b for a, b in zip(encrypted_bytes, extended_key))
    return decrypted_bytes.decode()

# add member username, password and name
def add_member():
    while True:
        try:
            member_info = int(input('How much member information do you want to add? '))
            for i in range(0, member_info):
                next_member_usn = 1
                for member_usn in sorted(member_usn_list):
                    if int(member_usn[2:]) != next_member_usn:  # find gaps
                        break
                    next_member_usn += 1  # if no gaps then move to next number
                member_usn = 'TP' + str(next_member_usn).zfill(6)
                print("Member username " + member_usn + " is generated.")
                member_pswd = member_usn.lower()
                print("Member password " + member_pswd + " is generated.")
                encrypted_member_pswd = xor_encrypt(member_pswd)
                member_name = str(input('Please enter the member name:')).title()
                while member_name == '' or not member_name.replace(' ', '').isalpha():
                    if member_name == '':
                        member_name = str(
                            input("Member's name cannot be empty. Please enter a name:")).title()
                    else:
                        member_name = str(
                            input(
                                "Member's name cannot include digits and special characters, only alphabet is allowed. Please enter a valid name:")).title()
                member_usn_list.append(member_usn)
                member_pswd_list.append(encrypted_member_pswd)
                member_name_list.append(member_name)
                print('Member list has been updated.')
                save_member()
                member_list = list(zip(member_usn_list, member_pswd_list, member_name_list))
                for i, (member_usn, member_pswd, member_name) in enumerate(
                        member_list):
                    print(member_usn, xor_decrypt(member_pswd), member_name)
            break
        except ValueError:
            print('Please enter an integer.')

def view_member():
    if member_usn_list and member_pswd_list and member_name_list != []:
        member_list = sorted(zip(member_usn_list, member_pswd_list, member_name_list))
        for i, (member_usn, member_pswd, member_name) in enumerate(
                member_list):
            print(i+1, member_usn, xor_decrypt(member_pswd), member_name)
    else:
        print('Sorry, the member list is empty.')
    time.sleep(2)

def get_search_select():
    while True:
        try:
            search_select = int(
                input('What would you like to search for?\n1. Username\n2. Name\n3. Back to previous menu'))
            if 1 <= search_select <= 3:
                return search_select
            else:
                print('Please enter an integer between 1 and 3.')
        except ValueError:
            print('Please enter an integer.')

def search_member_usn():
    search_usn = str(input('What username do you want to search?'))
    while search_usn == '':
        search_usn = input(
            'The username should not leave empty. Kindly enter the username of the member: ')
    else:
        found = False
        for i, (member_usn, member_pswd, member_name) in enumerate(
                zip(member_usn_list, member_pswd_list, member_name_list)):
            if (member_usn.lower()).startswith(search_usn.lower()):
                found = True
                print(member_usn, xor_decrypt(member_pswd), member_name)
        if found is not True:
            print('Sorry, the member is not in the list.')
        time.sleep(2)


def search_member_name():
    search_name = str(input('What member information do you want to search?'))
    while search_name == '':
        search_name = input(
            'The name should not leave empty. Kindly enter the name of the member: ')
    else:
        found = False
        for i, (member_usn, member_pswd, member_name) in enumerate(
                zip(member_usn_list, member_pswd_list, member_name_list)):
            if search_name.lower() in member_name.lower():
                found = True
                print(member_usn, xor_decrypt(member_pswd), member_name)
        if found is not True:
            print('Sorry, the member is not in the list.')
        time.sleep(2)


def search_member():
    while True:
        search_select = get_search_select()
        if search_select == 1:  # search by username
            search_member_usn()
        elif search_select == 2:  # search by name
            search_member_name()
        else:
            break

def get_row_edit():
    member_list = list(zip(member_usn_list, member_pswd_list, member_name_list))
    print('--------------------')
    for i, (member_usn, member_pswd, member_name) in enumerate(member_list):
        print(i + 1, member_usn, xor_decrypt(member_pswd), member_name)
    while True:
        try:
            num = int(input('What member information do you want to edit? Enter 1 for first row:'))
            if num <= len(member_list):
                return num
            else:
                print('Please type a valid row. This row does not exist in the list.')
        except ValueError:
            print('Please enter an integer.')

def get_key_edit():
    while True:
        try:
            key_to_edit = int(
                input('1. Edit username \n2. Edit password \n3. Edit name \nChoose an option.'))
            if 1 <= key_to_edit <= 3:
                return key_to_edit
            else:
                key_to_edit = print(
                    'Please enter a valid option.')
        except ValueError:
            print('Please enter an integer.')

def edit_member_usn(num):
    member_usn = str(input('Please enter a new username:')).upper()
    while member_usn in member_usn_list or member_usn == '' or not (len(member_usn) == 8 and member_usn[0] == 'T' and
                                                                    member_usn[1] == 'P' and member_usn[2:8].isdigit()):
        if member_usn in member_usn_list:
            member_usn = str(input(
                'The username exits in the list. Please enter a new username:')).upper()
        elif member_usn == '':
            member_usn = input(
                'The username should not leave empty. Kindly enter the username of the member: ').upper()
        else:
            member_usn = str(input(
                'Please follow this format: "TP123456" to enter an username:')).upper()

    member_usn_list[num - 1] = member_usn
    for i,(member_usn, member_pswd, member_name) in enumerate(zip(member_usn_list, member_pswd_list, member_name_list)):
        if member_usn == member_usn_list[num - 1]:
            member_pswd = member_usn.lower()
            member_pswd_list[i] = xor_encrypt(member_pswd)
            print(member_usn,member_pswd, member_name)
    print('Your new member information has been updated.')
    save_member()


def edit_member_pswd(num):
    member_pswd = str(input('Please enter a new password:'))
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`-]).{8,}$'
    while member_pswd == '' or (member_pswd == member_pswd_list[num - 1]) or re.match(pattern, member_pswd) is None:
        if member_pswd == '':
            member_pswd = str(
                input('Password cannot be empty. Please set a password.'))
        elif (member_pswd == member_pswd_list[num - 1]):
            member_pswd = str(input(
                'This password is same as the old password. Please enter a new password:'))
        else:
            member_pswd = (input(
                'This password is weak.\nPlease include at least one uppercase, one lowercase, one special character, one digit and must have at least 8 characters long: '))
    member_pswd = xor_encrypt(member_pswd)
    member_pswd_list[num - 1] = member_pswd
    for i, (member_usn, member_pswd, member_name) in enumerate(
            zip(member_usn_list, member_pswd_list, member_name_list)):
        if member_pswd == member_pswd_list[num - 1]:
            print(member_usn, xor_decrypt(member_pswd), member_name)
    print('Your new member information has been updated.')
    save_member()

def edit_member_name(num):
    member_name = str(input('Please enter new name:')).title()
    while member_name == '' or not member_name.replace(' ', '').isalpha() or (
            member_name == member_name_list[num - 1]):
        if member_name == '':
            member_name = str(
                input("Member's name cannot be empty. Please enter a name:")).title()
        elif not member_name.replace(' ', '').isalpha():
            member_name = str(
                input(
                    "Member's name cannot include digits and special characters, only alphabet is allowed. Please enter a valid name:")).title()
        else:
            member_name = str(input(
                'This name is same as the original name. Please enter a new name:')).title()
    member_name_list[num - 1] = member_name
    for i, (member_usn, member_pswd, member_name) in enumerate(
            zip(member_usn_list, member_pswd_list, member_name_list)):
        if member_name == member_name_list[num - 1]:
            print(member_usn, xor_decrypt(member_pswd), member_name)
    print('Your new member information has been updated.')
    save_member()

def edit_member():
    key_to_edit = get_key_edit()
    num = get_row_edit()
    if key_to_edit == 1:
        edit_member_usn(num)

    elif key_to_edit == 2:
        edit_member_pswd(num)

    else:
        edit_member_name(num)

def remove_member():
    member_list = sorted(list(zip(member_usn_list, member_pswd_list, member_name_list)))
    for i, (member_usn, member_pswd, member_name) in enumerate(member_list):
        print(i + 1, member_usn, xor_decrypt(member_pswd), member_name)
    while True:
        try:
            key_to_delete = int(input('Which row of member information do you want to delete?'))
            if key_to_delete <= len(member_list):
                original_index = list(member_list)[key_to_delete - 1]
                member_usn_list.remove(original_index[0])
                member_pswd_list.remove(original_index[1])
                member_name_list.remove(original_index[2])
                member_list = sorted(zip(member_usn_list, member_pswd_list, member_name_list))
                print('Member list has been deleted.')
                save_member()
                for i, (member_usn, member_pswd, member_name) in enumerate(member_list):
                    print(i + 1, member_usn, xor_decrypt(member_pswd), member_name)
                break
            else:
                print('Please type a valid row. This row does not exist in the list.')

        except ValueError:
            print('Please enter an integer.')


# add librarian username, password and name
def add_librarian():
    while True:
        try:
            librarian_info = int(input('How much librarian information do you want to add? '))
            for i in range(0, librarian_info):
                next_librarian_usn = 1
                for librarian_usn in sorted(librarian_usn_list):
                    if int(librarian_usn[1:]) != next_librarian_usn:  # find gaps
                        break
                    next_librarian_usn += 1  # if no gaps then move to next number
                librarian_usn = 'L' + str(next_librarian_usn).zfill(5)
                print("Librarian username " + librarian_usn + " is generated.")
                librarian_pswd = librarian_usn.lower()
                print("Librarian password " + librarian_pswd + " is generated.")
                encrypted_librarian_pswd = xor_encrypt(librarian_pswd)
                librarian_name = str(input('Please enter the librarian name:')).title()
                while librarian_name == '' or not librarian_name.replace(' ', '').isalpha():
                    if librarian_name == '':
                        librarian_name = str(
                            input("Librarian's name cannot be empty. Please enter a name:")).title()
                    else:
                        librarian_name = str(
                            input(
                                "Librarian's name cannot include digits and special characters, only alphabet is allowed. Please enter a valid name:")).title()
                librarian_usn_list.append(librarian_usn)
                librarian_pswd_list.append(encrypted_librarian_pswd)
                librarian_name_list.append(librarian_name)
                print('Librarian list has been updated.')
                save_librarian()
                librarian_list = list(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list))
                for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
                        librarian_list):
                    print(librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
            break
        except ValueError:
            print('Please enter an integer.')

def view_librarian():
    if librarian_usn_list and librarian_pswd_list and librarian_name_list != []:
        librarian_list = sorted(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list))
        for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
                librarian_list):
            print(i + 1, librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
    else:
        print('Sorry, the member list is empty.')
    time.sleep(2)

def search_librarian_usn():
    search_usn = str(input('What username do you want to search?'))
    while search_usn == '':
        search_usn = input(
            'The username should not leave empty. Kindly enter the username of the librarian: ')
    else:
        found = False
        for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
                zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
            if (librarian_usn.lower()).startswith(search_usn.lower()):
                found = True
                print(librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
        if found is not True:
            print('Sorry, the librarian is not in the list.')
        time.sleep(2)


def search_librarian_name():
    search_name = str(input('What librarian information do you want to search?'))
    while search_name == '':
        search_name = input(
            'The name should not leave empty. Kindly enter the name of the librarian: ')
    else:
        found = False
        for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
                zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
            if search_name.lower() in librarian_name.lower():
                found = True
                print(librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
        if found is not True:
            print('Sorry, the librarian is not in the list.')
        time.sleep(2)


def search_librarian():
    while True:
        search_select = get_search_select()
        if search_select == 1:  # search by username
            search_librarian_usn()
        elif search_select == 2:  # search by name
            search_librarian_name()
        else:
            break

def get_lib_row_edit():
    librarian_list = list(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list))
    print('--------------------')
    for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
            librarian_list):
        print(i + 1, librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
    while True:
        try:
            num = int(input('What librarian information do you want to edit? Enter 1 for first row:'))
            if num <= len(librarian_list):
                return num
            else:
                print('Please type a valid row. This row does not exist in the list.')
        except ValueError:
            print('Please enter an integer.')

def edit_librarian_usn(num):
    librarian_usn = str(input('Please enter a new username:')).upper()
    while librarian_usn in librarian_usn_list or librarian_usn == '' or not (len(librarian_usn) == 6 and librarian_usn[0] == 'L' and librarian_usn[1:].isdigit()):
        if librarian_usn in librarian_usn_list:
            librarian_usn = str(input(
                'The username exits in the list. Please enter a new username:')).upper()
        elif librarian_usn == '':
            librarian_usn = input(
                'The username should not leave empty. Kindly enter the username of the librarian: ').upper()
        else:
            librarian_usn = str(input(
                'Please follow this format: "L12345" to enter an username:')).upper()

    librarian_usn_list[num - 1] = librarian_usn
    for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
            zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
        if librarian_usn == librarian_usn_list[num - 1]:
            librarian_pswd = librarian_usn.lower()
            librarian_pswd_list[i] = xor_encrypt(librarian_pswd)
            print(librarian_usn, librarian_pswd, librarian_name)
    print('Your new librarian information has been updated.')
    save_librarian()

def edit_librarian_pswd(num):
    librarian_pswd = str(input('Please enter a new password:'))
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`-]).{8,}$'
    while librarian_pswd == '' or (librarian_pswd == librarian_pswd_list[num - 1]) or re.match(pattern, librarian_pswd) is None:
        if librarian_pswd == '':
            librarian_pswd = str(
                input('Password cannot be empty. Please set a password.'))
        elif (librarian_pswd == librarian_pswd_list[num - 1]):
            librarian_pswd = str(input(
                'This password is same as the old password. Please enter a new password:'))
        else:
            librarian_pswd = (input(
                'This password is weak.\nPlease include at least one uppercase, one lowercase, one special character, one digit and must have at least 8 characters long: '))
    librarian_pswd = xor_encrypt(librarian_pswd)
    librarian_pswd_list[num - 1] = librarian_pswd
    for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
            zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
        if librarian_pswd == librarian_pswd_list[num - 1]:
            print(librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
    print('Your new librarian information has been updated.')
    save_librarian()

def edit_librarian_name(num):
    librarian_name = str(input('Please enter new name:')).title()
    while librarian_name == '' or not librarian_name.replace(' ', '').isalpha() or (
            librarian_name == librarian_name_list[num - 1]):
        if librarian_name == '':
            librarian_name = str(
                input("Librarian's name cannot be empty. Please enter a name:")).title()
        elif not librarian_name.replace(' ', '').isalpha():
            librarian_name = str(
                input(
                    "Librarian's name cannot include digits and special characters, only alphabet is allowed. Please enter a valid name:")).title()
        else:
            librarian_name = str(input(
                'This name is same as the original name. Please enter a new name:')).title()
    librarian_name_list[num - 1] = librarian_name
    for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
            zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
        if librarian_name == librarian_name_list[num - 1]:
            print(librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
    print('Your new librarian information has been updated.')
    save_librarian()

def edit_librarian():
    key_to_edit = get_key_edit()
    num = get_lib_row_edit()
    if key_to_edit == 1:
        edit_librarian_usn(num)

    elif key_to_edit == 2:
        edit_librarian_pswd(num)

    else:
        edit_librarian_name(num)

def remove_librarian():
    librarian_list = sorted(list(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)))
    for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(librarian_list):
        print(i + 1, librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
    while True:
        try:
            key_to_delete = int(input('Which row of librarian information do you want to delete?'))
            if key_to_delete <= len(librarian_list):
                original_index = list(librarian_list)[key_to_delete - 1]
                librarian_usn_list.remove(original_index[0])
                librarian_pswd_list.remove(original_index[1])
                librarian_name_list.remove(original_index[2])
                librarian_list = sorted(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list))
                print('Librarian list has been deleted.')
                save_librarian()
                for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(librarian_list):
                    print(i + 1, librarian_usn, xor_decrypt(librarian_pswd), librarian_name)
                break
            else:
                print('Please type a valid row. This row does not exist in the list.')
        except ValueError:
            print('Please enter an integer.')

# add new book
def add_book(book_isbn, book_title, book_author, book_status):
    book_isbn_list.append(book_isbn)
    book_title_list.append(book_title)
    book_author_list.append(book_author)
    book_status_list.append(book_status)
    book_list = list(zip(book_isbn_list, book_title_list, book_author_list, book_status_list))
    print(list(book_list))

def calculate_overdue_fee(due_date, return_date):
    if isinstance(due_date, str):
        due_date = datetime.datetime.strptime(due_date, '%d-%m-%Y').date()
    if return_date is None:
        return_date = datetime.date.today()
    overdue_days = (return_date - due_date).days
    overdue_fee = 0.0
    if overdue_days > 0:
        if overdue_days == 1:
            overdue_fee = 2.00
        elif overdue_days == 2:
            overdue_fee = 3.00
        elif overdue_days == 3:
            overdue_fee = 4.00
        elif overdue_days == 4:
            overdue_fee = 5.00
        elif overdue_days == 5:
            overdue_fee = 6.00
        else:
            overdue_fee = 10.00
    return int(overdue_days) if overdue_days > 0 else 0, overdue_fee

def save_books():
    with open('books.txt', 'w') as file:
        no = 1
        for isbn, title, author, status in zip(book_isbn_list, book_title_list, book_author_list, book_status_list):
            file.write(f"{no}) Book ISBN: {isbn}, Book Title: {title}, Book Author: {author}, Book Status: {status}\n")
            no += 1

def save_book_loans():
    with open('book_loans.txt', 'w') as file:
        for loan in book_loan_list:
            file.write(f"{loan['member_id']}|{loan['book_isbn']}|{loan['loan_date']}|{loan['due_date']}\n")

def save_member():
    with open('member.txt', 'w') as file:
        no = 1
        member_list = list(zip(member_usn_list, member_pswd_list, member_name_list))
        for member_usn, member_pswd, member_name in sorted(member_list):
            file.write(f"{no}) Username: {member_usn}, Password: {member_pswd}, Name: {member_name}\n")
            no += 1

def save_librarian():
    with open('librarian.txt', 'w') as file:
        no = 1
        librarian_list = list(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list))
        for librarian_usn, librarian_pswd, librarian_name in sorted(librarian_list):
            file.write(f"{no}) Username: {librarian_usn}, Password: {librarian_pswd}, Name: {librarian_name}\n")
            no += 1

def get_admin_func():
    while True:
        try:
            admin_func = int(
                input(
                    'Please select an option.\n1. Member Information Management\n2. Librarian Information Management\n3. Log out'))
            if 1<= admin_func <=3:
                return admin_func
            else:
                print(
                    'Please insert number 1,2 or 3.')
        except ValueError:
            print(
                    'Invalid input, please enter an integer.')

def get_mim_option():
    while True:
        try:
            print('--------------------')
            mim = int(input(
                'Please select an option.\n1. Add new member information \n2. View all member information. \n3. Search member information '
                '\n4. Edit member information \n5. Remove member\n6. Back to previous menu'))
            if 1 <= mim <= 6:
                return mim
            else:
                print(
                    'Please enter number between 1 and 6.')
        except ValueError:
            print(
                'Invalid input, please enter an integer.')

def get_lim_option():
    while True:
        try:
            print('--------------------')
            lim = int(input(
                'Please select an option.\n1. Add new librarian information \n2. View all librarian information. \n3. Search librarian information '
                '\n4. Edit librarian information \n5. Remove librarian\n6. Back to previous menu'))
            if 1 <= lim <= 6:
                return lim
            else:
                print(
                    'Please enter number between 1 and 6.')
        except ValueError:
            print(
                'Invalid input, please enter an integer.')

def admin_menu():
    while True:
        admin_func = get_admin_func()
        while admin_func != 1 and admin_func != 2 and admin_func != 3:
            admin_func = int(input(
                'Please insert number 1,2 or 3. \n1. Member Information Management \n2. Librarian Information Management\n3. Log out'))
        else:
            if admin_func == 1: #member information management
                while True:
                    mim = get_mim_option()
                    if mim == 1:
                        add_member()
                        time.sleep(1)

                    elif mim == 2:  # view member info
                        view_member()

                    elif mim == 3:  # search member info
                        search_member()

                    elif mim == 4:  # edit member info
                        edit_member()
                        time.sleep(2)

                    elif mim == 5:  # remove member
                        remove_member()
                    else:
                        break

            elif admin_func == 2:  # librarian information management
                while True:
                    lim = get_lim_option()
                    if lim == 1:
                        add_librarian()
                        time.sleep(1)

                    elif lim == 2:  # view member info
                        view_librarian()

                    elif lim == 3:  # search member info
                        search_librarian()

                    elif lim == 4:  # edit member info
                        edit_librarian()
                        time.sleep(2)

                    elif lim == 5:  # remove member
                        remove_librarian()
                    else:
                        break
            else:
                break

def add_new_book():
    try:
        num_books = int(input('How many books do you want to add? '))
        for i in range(0, num_books):
            book_isbn = input('Please enter the ISBN of the book: ')
            while len(book_isbn) != 13 or not book_isbn.isdigit() or (book_isbn in book_isbn_list):
                if len(book_isbn) != 13:
                    book_isbn = input("ISBN must be 13 digits. Please try again: ")
                elif not book_isbn.isdigit():
                    book_isbn = input("ISBN must only contain digits. Please try again: ")
                else:
                    book_isbn = input("Book already exists in the catalogue!Try again:")
            else:
                book_title = input('Please enter the title of the book: ').title()
                while book_title == '':
                    book_title = input('The title should not leave empty. Please enter again: ').title()
                else:
                    book_author = input('Please enter the name of the author: ').title()
                    while book_author == '' or not book_author.replace(' ', '').isalpha():
                        if book_author == '':
                            book_author = input('The author should not leave empty. Please enter again: ').title()
                        else:
                            book_author = input('The author must only contain alphabets. Please try again: ').title()
                    else:
                        add_book(book_isbn, book_title, book_author, book_status)
                        print("Book added successfully!")
                        save_books()
    except ValueError:
        print("Please enter a valid number")
        time.sleep(1)

def view_book():
    if book_isbn_list and book_title_list and book_author_list != []:  # check if the list is not empty
        book_list = sorted(zip(book_isbn_list, book_title_list, book_author_list, book_status_list))
        for i, (book_isbn, book_title, book_author, book_status) in enumerate(book_list):
            print(i + 1, book_isbn, book_title, book_author, book_status)
    else:
        print("The list is empty")
    time.sleep(2)

def search_book():
    if not book_isbn_list:  # Check if the book list is empty
        print("There are no books in the list.")
        time.sleep(2)  # Give some time for the librarian to read the message
        librarian_dashboard()

    # search book in catalogue
    book_list = list(zip(book_isbn_list, book_title_list, book_author_list, book_status_list))
    search_option = int(input(
        'How would you like to search for the book?\n1. By ISBN\n2. By Title\n3. By Author\nChoose an option: '))
    while not (1 <= search_option <= 3):
        search_option = int(input('Enter a valid option\n1. By ISBN\n2. By Title\n3. By Author\nChoose an option: '))
    else:
        if search_option == 1:  # search by ISBN
            search_ISBN = input('Kindly enter the ISBN of the book: ')
            while search_ISBN == '':
                search_ISBN = input('The ISBN should not leave empty. Kindly enter the ISBN of the book: ')
            else:
                found = False
                for i, (book_isbn, book_title, book_author, book_status) in enumerate(book_list):
                    if book_isbn.startswith(search_ISBN):
                        found = True
                        print(i + 1, book_isbn, book_title, book_author, book_status)
                if found is not True:
                    print("Book does not exist")

        if search_option == 2:  # search by title
            search_title = input('Kindly enter the title of the book: ').title()
            while search_title == '':
                search_title = input('The title should not leave empty. Kindly enter the title of the book: ').title()
            else:
                found = False
                for i, (book_isbn, book_title, book_author, book_status) in enumerate(book_list):
                    if search_title.lower() in book_title.lower():
                        found = True
                        print(i + 1, book_isbn, book_title, book_author, book_status)
                if found is not True:
                    print("Book does not exist")

        if search_option == 3:  # search by author
            search_author = input('Kindly enter the author of the book: ').title()
            while search_author == '':
                search_author = input(
                    'The author should not leave empty. Kindly enter the author of the book: ').title()
            else:
                found = False
                for i, (book_isbn, book_title, book_author, book_status) in enumerate(book_list):
                    if search_author.lower() in book_author.lower():
                        found = True
                        print(i + 1, book_isbn, book_title, book_author, book_status)
                if found is not True:
                    print("Book does not exist")
    time.sleep(2)

def edit_book():
    if not book_isbn_list:  # Check if the book list is empty
        print("There are no books in the catalogue.")
        time.sleep(2)  # Give some time for the librarian to read the message
        librarian_dashboard()
    book_list = list(zip(book_isbn_list, book_title_list, book_author_list, book_status_list))
    for i, (book_isbn, book_title, book_author, book_status) in enumerate(book_list):
        print(i + 1, book_isbn, book_title, book_author, book_status)

    number = int(input('Which book would you like to enter?: '))
    while not number <= len(book_list):
        number = int(input('Please enter a valid row number: '))
    else:
        edit = int(
            input('Which information would like to edit? \n1. ISBN\n2. Book Title\n3. Book Author\nChoose an option: '))
        while not (1 <= edit <= 3):
            edit = int(input('Enter a valid option  \n1. ISBN\n2. Book Title\n3. Book Author\nChoose an option: '))
        else:
            if edit == 1:
                new_book_isbn = input('Please enter the new ISBN of the book: ')
                while (new_book_isbn in book_isbn_list) or len(new_book_isbn) != 13 or not new_book_isbn.isdigit():
                    if new_book_isbn in book_isbn_list:
                        new_book_isbn = input("The ISBN already exist in the list, Try again : ")
                    elif len(new_book_isbn) != 13:
                        new_book_isbn = input('ISBN must be 13 digits. Please try again: ')
                    else:
                        new_book_isbn = input('ISBN must only include digits. Please try again:')

                book_isbn_list[number - 1] = new_book_isbn
                book_list = zip(book_isbn_list, book_title_list, book_author_list, book_status_list)
                print(list(book_list)[number - 1])
                print("Your new information have been updated!")
                save_books()

            elif edit == 2:
                new_book_title = input('Please enter the new book title: ').title()
                while new_book_title == '' or new_book_title in book_title_list:
                    if new_book_title == '':
                        new_book_title = input('The book title cannot be empty. Please enter again: ').title()
                    else:
                        new_book_title = input("The book title already exist in the list, Try again: ").title()
                else:
                    book_title_list[number - 1] = new_book_title
                    book_list = zip(book_isbn_list, book_title_list, book_author_list, book_status_list)
                    print(list(book_list)[number - 1])
                    print("Your new information have been updated!")
                    save_books()

            elif edit == 3:
                new_book_author = input('Please enter the new book author name: ').title()
                while new_book_author == '' or (new_book_author in book_author_list) or not new_book_author.replace(' ',
                                                                                                                    '').isalpha():
                    if new_book_author in book_author_list:
                        new_book_author = input("The author already exist in the list, Try again: ").title()
                    elif new_book_author == '':
                        new_book_author = input("The author name cannot be empty. Please try again: ").title()
                    else:
                        new_book_author = input("The author must only include alphabets. Please try again: ").title()
                else:
                    book_author_list[number - 1] = new_book_author
                    book_list = zip(book_isbn_list, book_title_list, book_author_list, book_status_list)
                    print(list(book_list)[number - 1])
                    print("Your new information have been updated!")
                    save_books()

    time.sleep(2)

def remove_book():
    if not book_isbn_list:  # Check if the book list is empty
        print("There are no books in the catalogue. Please add books first.")
        time.sleep(2)  # Give some time for the librarian to read the message
        librarian_dashboard()

    book_list = sorted(list(zip(book_isbn_list, book_title_list, book_author_list, book_status_list)))
    for i, (book_isbn, book_title, book_author, book_status) in enumerate(book_list):
        print(i + 1, book_isbn, book_title, book_author, book_status)
    key_to_delete = int(input('Which row of book would you like to remove?'))
    while not key_to_delete <= len(book_list):
        key_to_delete = int(
            input('Please type a valid row. This row does not exist in the list.'))
    else:
        original_index = list(book_list)[key_to_delete - 1]
        book_isbn_list.remove(original_index[0])
        book_title_list.remove(original_index[1])
        book_author_list.remove(original_index[2])
        book_status_list.remove(original_index[3])
        book_list = sorted(zip(book_isbn_list, book_title_list, book_author_list, book_status_list))
        print('The row have been removed successfully!.')
        save_books()
        for i, (book_isbn, book_title, book_author, book_status) in enumerate(book_list):
            print(i + 1, book_isbn, book_title, book_author, book_status)

def perform_loan():
    print("--------------------")

    if not book_isbn_list:  # Check if the book list is empty
        print("There are no books in the catalogue. Please add books first.")
        time.sleep(2)  # Give some time for the librarian to read the message
        librarian_dashboard()

    num_loans = int(input('How many book loans do you want to enter?: '))
    for _ in range(0, num_loans):
        while True:
            member_usn = input('Enter the member ID: ').upper()
            while member_usn not in member_usn_list:
                member_usn = input('Member does not exist. Please try again: ').upper()
            else:
                # Check if member has any overdue books
                overdue_books = [loan for loan in book_loan_list if
                                 loan['member_id'] == member_usn and loan[
                                     'due_date'] < datetime.date.today()]
                # Check how many books user has borrowed
                borrowed_books = [book_loan for book_loan in book_loan_list if book_loan['member_id'] == member_usn]
                if overdue_books:
                    print("Member has overdue books. Cannot borrow books")
                    break
                elif len(borrowed_books) >= 5:
                    print("Sorry, member has already borrowed 5 books. Cannot borrow another book.")
                    break
                else:
                    book_isbn = input('Enter the ISBN of the book: ')
                    loaned_books_isbn = [loan['book_isbn'] for loan in book_loan_list]
                    while book_isbn not in book_isbn_list or book_isbn in loaned_books_isbn:
                        if book_isbn not in book_isbn_list:
                            book_isbn = input("Book does not exist. Please try again: ")
                        else:
                            book_isbn = input("Book is already on loan. Please enter another book: ")
                    else:
                        loan_date_input = input('Enter the loan date (in DD-MM-YYYY format): ')
                        while True:
                            try:
                                loan_date = datetime.datetime.strptime(loan_date_input, '%d-%m-%Y').date()
                                if loan_date > datetime.date.today():
                                    loan_date_input = input('Sorry,there is no advance book. Enter again: ')
                                else:
                                    due_date = loan_date + datetime.timedelta(days=14)
                                    # Add book into loan list
                                    return_date = None
                                    book_loan_list.append({
                                        'member_id': member_usn,
                                        'book_isbn': book_isbn,
                                        'loan_date': loan_date,
                                        'due_date': due_date,
                                        'return_date': return_date
                                    })
                                    print("Book loan added successfully.")
                                    save_book_loans()

                                    # Display the full list of loans
                                    print("Full list of loans:")
                                    for i, book_loan in enumerate(book_loan_list):
                                        print(i + 1, book_loan['member_id'], book_loan['book_isbn'],
                                              book_loan['loan_date'], book_loan['due_date'], book_loan['return_date'])
                                    book_list = list(
                                        zip(book_isbn_list, book_title_list, book_author_list,
                                            book_status_list))
                                    for i, (book_isbn, book_title, book_author, book_status) in enumerate(
                                            book_list):
                                        for book_loan in book_loan_list:
                                            if book_loan['book_isbn'] == book_isbn:
                                                if book_loan['return_date'] is None:
                                                    book_status = "On loan"
                                                else:
                                                    book_status = "Available"
                                        book_status_list[i] = book_status
                                    book_list = list(
                                        zip(book_isbn_list, book_title_list, book_author_list,
                                            book_status_list))
                                    break  # exit once loan done successfully
                            except ValueError:
                                loan_date_input = input(
                                    "Please enter a valid date format (DD-MM-YYYY). Please try again: ")

                        break


def return_book():
    if not book_loan_list:
        print("No books are currently on loan.")
        time.sleep(2)
        return

    # Display all current loans
    print("\nCurrent Book Loans:")
    print("No. | Member ID | ISBN | Book Title | Loan Date | Due Date")
    print("-" * 70)

    active_loans = []
    for i, loan in enumerate(book_loan_list, 1):
        if loan['return_date'] is None:  # Only show books that haven't been returned
            active_loans.append(loan)
            # Get book title from ISBN
            book_index = book_isbn_list.index(loan['book_isbn'])
            book_title = book_title_list[book_index]

            print(f"{i}. {loan['member_id']} | {loan['book_isbn']} | {book_title} | "
                  f"{loan['loan_date'].strftime('%d-%m-%Y')} | {loan['due_date'].strftime('%d-%m-%Y')}")

    if not active_loans:
        print("No active loans to return.")
        time.sleep(2)
        return

    try:
        loan_choice = int(input('\nEnter the number of the loan to process return: '))
        while not (1 <= loan_choice <= len(active_loans)):
            loan_choice = int(input('Invalid choice. Please enter a valid number: '))

        selected_loan = active_loans[loan_choice - 1]

        # Get return date
        return_date_input = input('Enter the return date (DD-MM-YYYY): ')
        while True:
            try:
                return_date = datetime.datetime.strptime(return_date_input, '%d-%m-%Y').date()
                if return_date < selected_loan['loan_date']:
                    return_date_input = input('Return date cannot be before loan date. Enter again: ')
                else:
                    break
            except ValueError:
                return_date_input = input('Invalid date format. Please use DD-MM-YYYY: ')

        # Calculate any overdue fees
        overdue_days, overdue_fee = calculate_overdue_fee(selected_loan['due_date'], return_date)

        # Update the loan record with return date
        for loan in book_loan_list:
            if (loan['member_id'] == selected_loan['member_id'] and
                    loan['book_isbn'] == selected_loan['book_isbn'] and
                    loan['loan_date'] == selected_loan['loan_date']):
                loan['return_date'] = return_date
        # Update book status to "Available"
        book_index = book_isbn_list.index(selected_loan['book_isbn'])
        book_status_list[book_index] = "Available"
        book_loan_list.remove(selected_loan)
        print("\nBook return processed successfully!")
        if overdue_days > 0:
            print(f"Overdue by {overdue_days} days")
            print(f"Overdue fee: RM {overdue_fee:.2f}")
        # Save updated records
        save_books()
        save_book_loans()

    except ValueError:
        print("Invalid input. Please enter a number.")
        time.sleep(2)

def librarian_dashboard():
    while True:
        librarian_func = int(
            input(
                'Welcome\n1. Book catalogue management\n2. Perform book loan process\n3. Log out\nChoose one:'))
        while librarian_func != 1 and librarian_func != 2 and librarian_func != 3:
            librarian_func = int(input(
                '\n1. Book catalogue management\n2. Perform book loan process\n3. Log out\nPlease insert number 1,2 or 3:'))
        else:
            if librarian_func == 1:  # Book catalogue management
                print("--------------------")
                while True:
                    bcm = int(input(
                        '\n1. Add new book into catalogue \n2. View all existing books in catalogue \n3. Search book from catalogue \n4. Edit book information '
                        '\n5. Remove book from catalogue\n6. Back to previous menu\nPlease select an option:'))
                    while not (1 <= bcm <= 6):
                        bcm = int(input(
                            '\n1. Add new book into catalogue \n2. View all existing books in catalogue \n3. Search book from catalogue \n4. Edit book information '
                            '\n5. Remove book from catalogue\n6. Back to previous menu\nPlease enter number between 1 and 6:'))
                    else:
                        if bcm == 1:  # add new book
                            add_new_book()

                        elif bcm == 2:
                            view_book()

                        elif bcm == 3:
                            search_book()

                        elif bcm ==4: #edit book information in catalogue
                            edit_book()

                        elif bcm == 5: #remove book from catalogue
                            remove_book()

                        else:
                            break


            elif librarian_func == 2:  # Perform book loan process
                books_func = int(input('\n1.Add loan book\n2.Returning book\nPlease Choose One:'))
                while books_func != 1 and books_func != 2:
                    books_func = int(input(
                        '\n1.Add loan book\n2.Returning book\nPlease Choose 1/2:'))
                if books_func == 1:
                    perform_loan()

                else:
                    return_book()

            else:
                break

def view_loaned_book(member_usn):
    print("--------------------")
    book_loan_list = []
    try:
        with open("book_loans.txt", "r") as file:
            for line in file:
                data = line.strip().split('|')
                if len(data) == 4:
                    file_member_usn, book_isbn, loan_date_str, due_date_str = data
                    loan_date = datetime.datetime.strptime(loan_date_str, "%Y-%m-%d").date()
                    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    book_loan_list.append({
                        'member_id': file_member_usn,
                        'book_isbn': book_isbn,
                        'loan_date': loan_date,
                        'due_date': due_date,
                        'return_date': None  # Assume the book hasn't been returned
                    })
    except FileNotFoundError:
        print("File not found.")
        return

    member_loans = [loan for loan in book_loan_list if
                      isinstance(loan, dict) and loan.get('member_id') == member_usn]
    if member_loans:
        print(f"Loaned Books by {member_usn}:")
        today_date = datetime.date.today()
        for i, book_loan in enumerate(member_loans, start=1):
            return_date = book_loan.get('return_date', today_date)
            overdue_days, overdue_fee = calculate_overdue_fee(book_loan['due_date'], return_date)
            status = 'Returned' if book_loan['return_date'] else ('Overdue' if overdue_days > 0 else 'On time')

            print(f"{i} Member ID: {book_loan['member_id']}")
            print(f"Book ISBN: {book_loan['book_isbn']}")
            print(f"Loan Date: {book_loan['loan_date']}")
            print(f"Due Date: {book_loan['due_date']}")
            print(f"Return Date: {book_loan['return_date']}")
            print(f"Overdue Days: {overdue_days}")
            print(f"Overdue Fee: RM {overdue_fee:.2f}")
            print(f"Status: {status}")
            print("                    ")

    else:
        print(f'No loaned book by member {member_usn}')
        time.sleep(2)

def member_dashboard(member_usn):
    while True:
        member_func = int(
            input(
                'Please select an option.\n1. View current loaned books\n2. Update profile information\n3. Search book catalogues\n4. Log out '))
        if not (1 <= member_func <= 4):
            member_func = int(input(
                'Please insert number 1-4\n 1. View current loaned books\n2. Update profile information\n3. Search book catalogues\n4. Log out '))
        else:
            if member_func == 1:  # view loaned book
                view_loaned_book(member_usn)

            elif member_func == 2:  # update profile info
                print("--------------------")
                num = member_usn_list.index(member_usn) + 1
                print("Current information:")
                print("Username:", member_usn_list[num - 1])
                print("Password:", xor_decrypt(member_pswd_list[num - 1]))
                print("Name:", member_name_list[num - 1])

                key_to_edit = get_key_edit()
                if key_to_edit ==1:
                    member_usn = str(input('Please enter a new username:')).upper()
                    while member_usn in member_usn_list or member_usn == '' or not (
                            len(member_usn) == 8 and member_usn[0] == 'T' and
                            member_usn[1] == 'P' and member_usn[2:8].isdigit()):
                        if member_usn in member_usn_list:
                            member_usn = str(input(
                                'The username exits in the list. Please enter a new username:')).upper()
                        elif member_usn == '':
                            member_usn = input(
                                'The username should not leave empty. Kindly enter the username of the member: ').upper()
                        else:
                            member_usn = str(input(
                                'Please follow this format: "TP123456" to enter an username:')).upper()

                    member_usn_list[num - 1] = member_usn
                    for i, (member_usn, member_pswd, member_name) in enumerate(
                            zip(member_usn_list, member_pswd_list, member_name_list)):
                        if member_usn ==member_usn_list[num-1]:
                            print(member_usn, xor_decrypt(member_pswd), member_name)
                    print('Your new member information has been updated.')
                    save_member()
                elif key_to_edit ==2:
                    edit_member_pswd(num)
                elif key_to_edit ==3:
                    edit_member_name(num)
                else:
                    break
                time.sleep(2)


            elif member_func == 3:  # search book catalogue
                search_book()

            else:
                print('Logging out...')
                break

def select_role():
    while True:
        try:
            role = int(input('1. System Admin\n2. Librarian\n3. Library Member\nChoose your role.\nPress 4 to exit.'))
            if 1 <= role <= 4:
                return role
            else:
                print('Please select an option 1-4.')
        except ValueError:
            print('Please enter an integer.')


def admin_login():
    admin_input = str(input('Welcome. Please enter your username: '))
    while admin_input != admin_username:  # admin username input must be same as fixed admin username
        admin_input = str(input('Please enter a valid admin username.'))
    else:  # can change admin password or directly log in
        while True:
            try:
                admin_pwd_select = int(input('1. Enter password. \n2. Change password. \nChoose one option.'))
                if admin_pwd_select == 1 or admin_pwd_select == 2:
                    return admin_pwd_select
                else:
                    print('Please enter a valid option.')
            except ValueError:
                print('Please enter an integer.')

def enter_admin_pswd():
    admin_pwd_input = str(input('Please enter your password: '))
    while admin_pwd_input != admin_password:
        admin_pwd_input = str(input('Please enter correct password: '))
    else:
        admin_menu()

def change_admin_pswd():
    global admin_password
    admin_new_pwd = input('Please set your new password:')
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`-]).{8,}$'
    while admin_new_pwd == admin_password or re.match(pattern,
                                                      admin_new_pwd) is None or admin_new_pwd == '':
        if admin_password == admin_new_pwd:
            admin_new_pwd = (
                input('This password is same as the old password. Please set your new password: '))
        elif admin_new_pwd == '':
            admin_new_pwd = str(
                input('Password cannot be empty. Please set a password.'))
        else:
            admin_new_pwd = (input(
                'This password is weak.\nPlease include at least one uppercase, one lowercase, one special character, one digit and must have at least 8 characters long: '))
    else:
        admin_password = admin_new_pwd
        print('You have successfully set a new password. Now you will be redirected to login page.')
        admin_input = str(input('Welcome. Please enter your username: '))
        while admin_input != admin_username:  # admin username input must be same as fixed admin username
            admin_input = str(input('Please enter a valid admin username.'))
        else:
            admin_pwd_input = str(input('Please enter your password: '))
            while admin_pwd_input != admin_password:
                admin_pwd_input = str(input('Please enter correct password: '))
            else:
                admin_menu()

def librarian_login():
    resetBookList()
    librarian_list = sorted(list(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)))
    librarian_usn_input = input('Please insert your username:')
    while librarian_usn_input not in librarian_usn_list:
        librarian_usn_input = input('Invalid username. Please insert valid username:')
    else:  # can change admin password or directly log in
        while True:
            try:
                for i,(librarian_usn, librarian_pswd, librarian_name) in enumerate(zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
                    if librarian_usn_input == librarian_usn:
                        print('Your password is ', xor_decrypt(librarian_pswd))
                        librarian_pwd_select = int(input('1. Enter password.\n2. Change password.\nChoose one option.'))
                        if librarian_pwd_select == 1 or librarian_pwd_select == 2:
                            return librarian_usn_input,librarian_pwd_select
                        else:
                            print('Please enter a valid option.')
            except ValueError:
                print('Please enter an integer.')
def enter_librarian_pswd(librarian_usn_input):
    for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
            zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
        if librarian_usn_input == librarian_usn:
            librarian_pwd_input = str(input('Please enter your password: '))
            while librarian_pwd_input != xor_decrypt(librarian_pswd):
                librarian_pwd_input = str(input('Please enter correct password: '))
            else:
                print('Login successfully.')
                librarian_dashboard()
                return
def change_librarian_pswd(librarian_usn_input):
    for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
            zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
        if librarian_usn_input == librarian_usn:
            librarian_new_pwd = str(input('Please set your new password:'))
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`-]).{8,}$'
            while librarian_new_pwd == xor_decrypt(librarian_pswd) or re.match(pattern,
                                                                  librarian_new_pwd) is None or librarian_new_pwd == '':
                if librarian_new_pwd == xor_decrypt(librarian_pswd):
                    librarian_new_pwd = (input(
                        'This password is same as the old password. Please set your new password: '))
                elif librarian_new_pwd == '':
                    librarian_new_pwd = str(
                        input('Password cannot be empty. Please set a password.'))
                else:
                    librarian_new_pwd = (input(
                        'This password is weak.\nPlease include at least one uppercase, one lowercase, one special character, one digit and must have at least 8 characters long: '))
            else:
                print('You have successfully set a new password. Now you will be redirected to login page.')
                librarian_new_pwd = xor_encrypt(librarian_new_pwd)
                librarian_pswd_list[i] = librarian_new_pwd
                save_librarian()
                librarian_usn_input = str(input('Welcome. Please enter your username: '))
                for i, (librarian_usn, librarian_pswd, librarian_name) in enumerate(
                        zip(librarian_usn_list, librarian_pswd_list, librarian_name_list)):
                    if librarian_usn_input == librarian_usn:
                        while librarian_usn_input != librarian_usn:  # admin username input must be same as fixed admin username
                            librarian_usn_input = str(input('Please enter a valid member username.'))
                        else:
                            librarian_pwd_input = str(input('Please enter your password: '))
                            while librarian_pwd_input != xor_decrypt(librarian_new_pwd):
                                librarian_pwd_input = str(input('Please enter correct password: '))
                            else:
                                print('Login successfully.')
                                librarian_dashboard()
                                return

def member_login():
    member_list = sorted(list(zip(member_usn_list, member_pswd_list, member_name_list)))
    member_usn_input = input('Please insert your username:')
    while member_usn_input not in member_usn_list:
        member_usn_input = input('Invalid username. Please insert valid username:')
    else:  # can change admin password or directly log in
        while True:
            try:
                for i,(member_usn, member_pswd, member_name) in enumerate(zip(member_usn_list, member_pswd_list, member_name_list)):
                    if member_usn_input == member_usn:
                        print('Your password is ', xor_decrypt(member_pswd))
                        member_pwd_select = int(input('1. Enter password.\n2. Change password.\nChoose one option.'))
                        if member_pwd_select == 1 or member_pwd_select == 2:
                            return member_usn_input,member_pwd_select
                        else:
                            print('Please enter a valid option.')
            except ValueError:
                print('Please enter an integer.')

def enter_member_pswd(member_usn_input):
    for i, (member_usn, member_pswd, member_name) in enumerate(zip(member_usn_list, member_pswd_list, member_name_list)):
        if member_usn_input == member_usn:
            member_pwd_input = str(input('Please enter your password: '))
            while member_pwd_input != xor_decrypt(member_pswd):
                member_pwd_input = str(input('Please enter correct password: '))
            else:
                print('Login successfully.')
                member_dashboard(member_usn)
                return
def change_member_pswd(member_usn_input):
    for i, (member_usn, member_pswd, member_name) in enumerate(
            zip(member_usn_list, member_pswd_list, member_name_list)):
        if member_usn_input == member_usn:
            member_new_pwd = str(input('Please set your new password:'))
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`-]).{8,}$'
            while member_new_pwd == xor_decrypt(member_pswd) or re.match(pattern,
                                                            member_new_pwd) is None or member_new_pwd == '':
                if member_new_pwd == xor_decrypt(member_pswd):
                    member_new_pwd = (input(
                        'This password is same as the old password. Please set your new password: '))
                elif member_new_pwd == '':
                    member_new_pwd = str(
                        input('Password cannot be empty. Please set a password.'))
                else:
                    member_new_pwd = input(
                        'This password is weak.\nPlease include at least one uppercase, one lowercase, one special character, one digit and must have at least 8 characters long: ')
            else:
                print('You have successfully set a new password. Now you will be redirected to login page.')
                member_new_pwd = xor_encrypt(member_new_pwd)
                member_pswd_list[i] = member_new_pwd
                save_member()
                member_usn_input = str(input('Welcome. Please enter your username: '))
                for i, (member_usn, member_pswd, member_name) in enumerate(zip(member_usn_list, member_pswd_list, member_name_list)):
                    if member_usn_input == member_usn:
                        while member_usn_input != member_usn:  # admin username input must be same as fixed admin username
                            member_usn_input = str(input('Please enter a valid member username.'))
                        else:
                            member_pwd_input = str(input('Please enter your password: '))
                            while member_pwd_input != xor_decrypt(member_new_pwd):
                                member_pwd_input = str(input('Please enter correct password: '))
                            else:
                                print('Login successfully.')
                                member_dashboard(member_usn)
                                return



while True:
    resetMemberList()
    resetLibrarianlist()
    resetBookList()
    resetBookLoanList()

    role = select_role()
    if role == 1: #admin
        admin_pwd_select = admin_login()
        if admin_pwd_select == 1:
            enter_admin_pswd()
        else:
            change_admin_pswd()


    elif role == 2: #librarian
        librarian_usn_input,librarian_pwd_select = librarian_login()
        if librarian_pwd_select == 1:
            enter_librarian_pswd(librarian_usn_input)
        else:
            change_librarian_pswd(librarian_usn_input)


    elif role == 3: #member
        member_usn_input, member_pwd_select = member_login()
        if member_pwd_select == 1:
            enter_member_pswd(member_usn_input)
        else:
            change_member_pswd(member_usn_input)


    else:
        break
