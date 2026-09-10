const students = {
    "010001": {
        name: "Nguyễn Minh Anh",
        scores: [
            { name: "Toán", score: 8.5 },
            { name: "Ngữ văn", score: 8.0 },
            { name: "Ngoại ngữ", score: 9.0 },
            { name: "Vật lý", score: 8.25 },
        ],
    },
    "010002": {
        name: "Trần Hoàng Nam",
        scores: [
            { name: "Toán", score: 7.25 },
            { name: "Ngữ văn", score: 7.5 },
            { name: "Ngoại ngữ", score: 6.75 },
            { name: "Hóa học", score: 8.0 },
        ],
    },
};

const form = document.querySelector("#score-form");
const formMessage = document.querySelector("#form-message");
const resultSection = document.querySelector("#result");
const subjectsSection = document.querySelector("#subjects");
const tableBody = document.querySelector("#score-table-body");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const registrationNumber = document.querySelector("#registration-number").value.trim();
    const student = students[registrationNumber];

    if (!student) {
        resultSection.hidden = true;
        subjectsSection.hidden = true;
        formMessage.textContent = "Không tìm thấy số báo danh. Hãy thử 010001 hoặc 010002.";
        formMessage.className = "form-message error";
        return;
    }

    const total = student.scores.reduce((sum, subject) => sum + subject.score, 0);
    const average = total / student.scores.length;

    document.querySelector("#student-name").textContent = student.name;
    document.querySelector("#result-registration-number").textContent = registrationNumber;
    document.querySelector("#total-score").textContent = `${total.toFixed(2)} điểm`;
    document.querySelector("#average-score").textContent = `${average.toFixed(2)} điểm`;
    document.querySelector("#classification").textContent = average >= 8 ? "Tốt" : "Khá";
    tableBody.innerHTML = student.scores.map((subject, index) => `
        <tr><td>${index + 1}</td><td>${subject.name}</td><td>${subject.score.toFixed(2)}</td></tr>
    `).join("");

    formMessage.textContent = "Đã tìm thấy kết quả.";
    formMessage.className = "form-message success";
    resultSection.hidden = false;
    subjectsSection.hidden = false;
});