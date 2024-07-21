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
            data.forEach((score, index) => {
                const row = table.insertRow(-1);
                row.insertCell(0).textContent = index + 1;
                row.insertCell(1).textContent = score.player_name;
                row.insertCell(2).textContent = score.score;
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.body.innerHTML += `<p>Error loading high scores: ${error.message}. Please try again later.</p>`;
        });
}

document.addEventListener('DOMContentLoaded', fetchHighScores);