# 🚌 Cloud-Based Bus Pass System

A web-based bus ticket booking system developed using Flask and SQLite. The application allows users to book bus tickets, select routes, choose the number of tickets, select a journey date and payment method, and view or delete existing bookings.

The application is deployed on the cloud using Render.

## 📌 Project Overview

The Cloud-Based Bus Pass System provides a simple online interface for managing bus ticket bookings.

Users can:

- Enter their name
- Select a bus route
- Select the number of tickets
- Select a journey date
- Select a payment method
- View booking details
- Delete bookings
- Check available seats

The system also prevents users from booking more tickets than the available seats.

## ✨ Features

### 1. Ticket Booking
Users can book tickets by providing the required journey and passenger details.

### 2. Multiple Bus Routes

The system currently supports:

| Bus Route | Fare per Ticket |
|---|---:|
| Bengaluru to Mysuru | ₹150 |
| Bengaluru to Kanakapura | ₹80 |
| Bengaluru to Ramanagara | ₹70 |

### 3. Automatic Price Calculation

The total price is calculated automatically:

`Total Price = Number of Tickets × Fare per Ticket`

### 4. Seat Availability

The system starts with 50 available seats.

When tickets are booked, the available seat count decreases automatically.

### 5. Overbooking Prevention

The system prevents users from booking more tickets than the available seats.

Both the web form and server-side validation are used.

### 6. Booking ID

Every successful booking receives a unique Booking ID.

### 7. Booking Management

All current bookings are displayed in a table containing:

- Booking ID
- Passenger Name
- Bus Route
- Number of Tickets
- Total Price
- Journey Date
- Payment Method

### 8. Delete Booking

Users can delete a booking. When a booking is deleted, the corresponding seats become available again.

## 🛠️ Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Git
- GitHub
- Render
- Gunicorn

## 📂 Project Structure

```text
CodeAlpha_BusPass/
│
├── app.py
├── bus.db
├── requirements.txt
├── README.md
│
└── static/
    └── style.css