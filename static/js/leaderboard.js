function fetchHighScores() {
    fetch('/high_scores')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const table = document.getElementById('scoreTable');
            // Xóa dữ liệu cũ
            while (table.rows.length > 1) {
                table.deleteRow(1);
            }
            // Thêm dữ liệu mới
            if (data.length === 0) {
                const row = table.insertRow(-1);
                const cell = row.insertCell(0);
                cell.colSpan = 3;
                cell.textContent = "No high scores yet!";
            } else {
                data.forEach((score, index) => {
                    if (index < 5) { // Chỉ hiển thị top 5
                        const row = table.insertRow(-1);
                        row.insertCell(0).textContent = index + 1;
                        row.insertCell(1).textContent = score.player_name;
                        row.insertCell(2).textContent = score.score.toLocaleString(); // Định dạng số
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessage = document.createElement('p');
            errorMessage.textContent = `Error loading high scores: ${error.message}. Please try again later.`;
            document.body.appendChild(errorMessage);
        });
}

document.addEventListener('DOMContentLoaded', fetchHighScores);

// Thêm hàm này nếu bạn muốn cập nhật bảng xếp hạng định kỳ
function startPeriodicUpdate() {
    setInterval(fetchHighScores, 60000); // Cập nhật mỗi 60 giây
}

document.addEventListener('DOMContentLoaded', () => {
    fetchHighScores();
    startPeriodicUpdate();
});