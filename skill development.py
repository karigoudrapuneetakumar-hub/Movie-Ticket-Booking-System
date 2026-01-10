import queue

booking_stack = []
booking_queue = queue.Queue()

def load_movies():
    try:
        with open("movies.txt","r") as f:
            movies={}
            for line in f:
                name,times=line.strip().split(":")
                movies[name]=times.split(",")
            return movies
    except:
        return {"Avengers":["10:00 AM","1:00 PM","6:00 PM"],
                "Inception":["11:00 AM","3:00 PM","8:00 PM"],
                "Interstellar":["9:30 AM","2:30 PM","7:30 PM"]}

def save_movies(movies):
    with open("movies.txt","w") as f:
        for name,times in movies.items():
            f.write(name+":"+ ",".join(times)+"\n")

def load_seats():
    try:
        with open("seats.txt","r") as f:
            seats=[]
            for line in f:
                seats.append(list(line.strip()))
            return seats
    except:
        return [["0"]*5 for _ in range(5)]

def save_seats(seats):
    with open("seats.txt","w") as f:
        for row in seats:
            f.write("".join(row)+"\n")

def save_booking(ticket):
    with open("bookings.txt","a") as f:
        f.write(ticket+"\n")

def display_seats(seats):
    print("\nSeat Layout (0 = Available, 1 = Booked)")
    for i,row in enumerate(seats):
        print(i," ".join(row))

def book_ticket():
    movies=load_movies()
    seats=load_seats()

    print("\nAvailable Movies:")
    for i,m in enumerate(movies.keys()):
        print(i+1,m)

    choice=int(input("\nSelect movie: "))
    movie=list(movies.keys())[choice-1]

    print("\nShow Timings:")
    for i,t in enumerate(movies[movie]):
        print(i+1,t)

    show=int(input("\nSelect show timing: "))
    show_time=movies[movie][show-1]

    display_seats(seats)
    row=int(input("\nEnter seat row: "))
    col=int(input("Enter seat column: "))

    if seats[row][col]=="1":
        print("❌ Seat already booked!")
        return

    seats[row][col]="1"
    ticket=f"{movie} | {show_time} | Seat({row},{col})"
    
    booking_stack.append(ticket)
    booking_queue.put(ticket)

    save_seats(seats)
    save_booking(ticket)

    print("\n🎟 Ticket Confirmed!")
    print(ticket)

def undo_booking():
    if not booking_stack:
        print("⚠ No bookings to undo!")
        return
    last=booking_stack.pop()
    print("\n↩ Booking undone:",last)

def view_last_booking():
    if not booking_stack:
        print("⚠ No bookings yet!")
    else:
        print("\n📌 Last Booking:",booking_stack[-1])

def view_booking_queue():
    if booking_queue.empty():
        print("⚠ Queue empty!")
        return
    print("\n🎫 Current Booking Queue:")
    temp=list(booking_queue.queue)
    for t in temp:
        print(t)

def main():
    while True:
        print("\n1.Book Ticket\n2.Undo Booking\n3.View Last Booking\n4.View Booking Queue\n5.Exit")
        ch=int(input("Enter choice: "))
        if ch==1:
            book_ticket()
        elif ch==2:
            undo_booking()
        elif ch==3:
            view_last_booking()
        elif ch==4:
            view_booking_queue()
        elif ch==5:
            print("Exiting...")
            break
        else:
            print("Invalid!")

main()
