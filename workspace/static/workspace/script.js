let currentDate = new Date();

const calendar = document.getElementById("calendar");
const monthYear = document.getElementById("monthYear");

const previousMonth =
    document.getElementById("previousMonth");

const nextMonth =
    document.getElementById("nextMonth");


function formatDate(year, month, day) {

    const monthString =
        String(month + 1).padStart(2, "0");

    const dayString =
        String(day).padStart(2, "0");

    return `${year}-${monthString}-${dayString}`;
}


function showCalendar() {

    calendar.innerHTML = "";

    const year = currentDate.getFullYear();

    const month = currentDate.getMonth();

    const monthName = currentDate.toLocaleString(
        "default",
        {
            month: "long"
        }
    );

    monthYear.innerText =
        `${monthName} ${year}`;


    const firstDay =
        new Date(year, month, 1).getDay();

    const daysInMonth =
        new Date(year, month + 1, 0).getDate();


    // Empty boxes before first day

    for (let i = 0; i < firstDay; i++) {

        const emptyDay =
            document.createElement("div");

        emptyDay.classList.add("empty-day");

        calendar.appendChild(emptyDay);
    }


    // Create calendar days

    for (
        let day = 1;
        day <= daysInMonth;
        day++
    ) {

        const dateString =
            formatDate(year, month, day);

        const dayBox =
            document.createElement("div");

        dayBox.classList.add("calendar-day");


        const number =
            document.createElement("strong");

        number.innerText = day;

        dayBox.appendChild(number);


        const dayBookings =
            bookings.filter(
                booking =>
                    booking.date === dateString
            );


        if (dayBookings.length > 0) {

            dayBox.classList.add("booked");

            dayBox.addEventListener(
                "click",
                function () {

                    showBookingDetails(
                        dateString,
                        dayBookings
                    );

                }
            );

        } else {

            dayBox.classList.add("free");

            dayBox.addEventListener(
                "click",
                function () {

                    showFreeDate(dateString);

                }
            );

        }


        calendar.appendChild(dayBox);
    }
}


function showBookingDetails(
    date,
    dayBookings
) {

    const modal =
        document.getElementById("bookingModal");

    const modalDate =
        document.getElementById("modalDate");

    const modalBookings =
        document.getElementById("modalBookings");


    modalDate.innerText =
        `Bookings for ${date}`;

    modalBookings.innerHTML = "";


    dayBookings.forEach(
        function (booking) {

            const bookingDiv =
                document.createElement("div");

            bookingDiv.classList.add(
                "modal-booking"
            );

            bookingDiv.innerHTML = `

                <h3>
                    ${booking.purpose}
                </h3>

                <p>
                    <strong>Department:</strong>
                    ${booking.department}
                </p>

                <p>
                    <strong>Time:</strong>
                    ${booking.start}
                    -
                    ${booking.end}
                </p>

                <p>
                    <strong>Status:</strong>
                    ${booking.status}
                </p>

            `;

            modalBookings.appendChild(
                bookingDiv
            );
        }
    );


    modal.style.display = "block";
}


function showFreeDate(date) {

    const modal =
        document.getElementById("bookingModal");

    const modalDate =
        document.getElementById("modalDate");

    const modalBookings =
        document.getElementById("modalBookings");


    modalDate.innerText =
        `${date}`;

    modalBookings.innerHTML = `

        <div class="free-message">

            <h3>Available</h3>

            <p>
                This resource is currently
                free on this date.
            </p>

        </div>

    `;


    modal.style.display = "block";
}


document
    .getElementById("closeModal")
    .onclick = function () {

        document.getElementById(
            "bookingModal"
        ).style.display = "none";

    };


window.onclick = function(event) {

    const modal =
        document.getElementById("bookingModal");

    if (event.target === modal) {

        modal.style.display = "none";

    }
};


previousMonth.onclick = function() {

    currentDate.setMonth(
        currentDate.getMonth() - 1
    );

    showCalendar();
};


nextMonth.onclick = function() {

    currentDate.setMonth(
        currentDate.getMonth() + 1
    );

    showCalendar();
};


if (calendar) {

    showCalendar();

}