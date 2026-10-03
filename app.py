from flask import Flask, request
import sqlite3

app = Flask(__name__)

TOTAL_SEATS = 50


def create_database():
    connection = sqlite3.connect("bus.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bus_name TEXT NOT NULL,
            tickets INTEGER NOT NULL,
            price INTEGER NOT NULL,
            journey_date TEXT NOT NULL,
            payment_method TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_database()


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    connection = sqlite3.connect("bus.db")

    bookings = connection.execute(
        "SELECT id, name, bus_name, tickets, price, journey_date, payment_method FROM bookings"
    ).fetchall()

    total_booked = sum(booking[3] for booking in bookings)
    available_seats = TOTAL_SEATS - total_booked

    connection.close()

    if request.method == "POST":

        name = request.form["name"]
        bus_name = request.form["bus_name"]
        tickets = int(request.form["tickets"])
        journey_date = request.form["journey_date"]
        payment_method = request.form["payment_method"]

        fares = {
            "Bengaluru to Mysuru": 150,
            "Bengaluru to Kanakapura": 80,
            "Bengaluru to Ramanagara": 70
        }

        if tickets > available_seats:

            message = (
                "Not enough seats available! "
                "Only " + str(available_seats) + " seats are available."
            )

        else:

            price_per_ticket = fares[bus_name]
            total_price = tickets * price_per_ticket

            connection = sqlite3.connect("bus.db")

            cursor = connection.execute(
                """
                INSERT INTO bookings
                (name, bus_name, tickets, price, journey_date, payment_method)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    bus_name,
                    tickets,
                    total_price,
                    journey_date,
                    payment_method
                )
            )

            booking_id = cursor.lastrowid

            connection.commit()
            connection.close()

            message = (
                "🎫 Booking Confirmed! "
                "Booking ID: " + str(booking_id) +
                " | Route: " + bus_name +
                " | Tickets: " + str(tickets) +
                " | Journey Date: " + journey_date +
                " | Payment: " + payment_method +
                " | Total Price: ₹" + str(total_price)
            )

    connection = sqlite3.connect("bus.db")

    bookings = connection.execute(
        "SELECT id, name, bus_name, tickets, price, journey_date, payment_method FROM bookings"
    ).fetchall()

    connection.close()

    total_booked = sum(booking[3] for booking in bookings)
    available_seats = TOTAL_SEATS - total_booked

    table = ""

    for booking in bookings:

        table += f"""
        <tr>
            <td>{booking[0]}</td>
            <td>{booking[1]}</td>
            <td>{booking[2]}</td>
            <td>{booking[3]}</td>
            <td>₹{booking[4]}</td>
            <td>{booking[5]}</td>
            <td>{booking[6]}</td>
            <td>
                <a href="/delete/{booking[0]}">Delete</a>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Cloud-Based Bus Pass System</title>

        <link rel="stylesheet" href="/static/style.css">

    </head>

    <body>

        <div class="container">

            <h1>🚌 Cloud-Based Bus Pass System</h1>

            <h2>Book Your Bus Ticket</h2>

            <p>
                <strong>Available Seats: {available_seats}</strong>
            </p>

            <form method="POST">

                <label>Name:</label>

                <input
                    type="text"
                    name="name"
                    required
                >

                <br><br>

                <label>Bus Route:</label>

                <select name="bus_name" required>

                    <option value="">
                        Select Bus Route
                    </option>

                    <option value="Bengaluru to Mysuru">
                        Bengaluru to Mysuru - ₹150
                    </option>

                    <option value="Bengaluru to Kanakapura">
                        Bengaluru to Kanakapura - ₹80
                    </option>

                    <option value="Bengaluru to Ramanagara">
                        Bengaluru to Ramanagara - ₹70
                    </option>

                </select>

                <br><br>

                <label>Number of Tickets:</label>

                <input
                    type="number"
                    name="tickets"
                    min="1"
                    max="{available_seats}"
                    required
                >

                <br><br>

                <label>Journey Date:</label>

                <input
                    type="date"
                    name="journey_date"
                    required
                >

                <br><br>

                <label>Payment Method:</label>

                <select name="payment_method" required>

                    <option value="">
                        Select Payment Method
                    </option>

                    <option value="UPI">
                        UPI
                    </option>

                    <option value="Card">
                        Card
                    </option>

                    <option value="Cash">
                        Cash
                    </option>

                </select>

                <br><br>

                <button type="submit">
                    Book Ticket
                </button>

            </form>

            <h3>{message}</h3>

            <hr>

            <h2>Booked Tickets</h2>

            <table>

                <tr>
                    <th>Booking ID</th>
                    <th>Name</th>
                    <th>Bus Route</th>
                    <th>Tickets</th>
                    <th>Total Price</th>
                    <th>Journey Date</th>
                    <th>Payment</th>
                    <th>Action</th>
                </tr>

                {table}

            </table>

        </div>

    </body>

    </html>
    """


@app.route("/delete/<int:booking_id>")
def delete_booking(booking_id):

    connection = sqlite3.connect("bus.db")

    connection.execute(
        "DELETE FROM bookings WHERE id = ?",
        (booking_id,)
    )

    connection.commit()
    connection.close()

    return """
    <script>
        window.location.href = "/";
    </script>
    """


if __name__ == "__main__":

    app.run(debug=True)