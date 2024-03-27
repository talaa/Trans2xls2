function uploadFile() {
            var form = document.getElementById('uploadForm');
            var formData = new FormData(form);
//   /process_file
            fetch('/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('outputTable').innerHTML = data.table_html;
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }

// Initialize your Lottie animation
// Example: lottie.loadAnimation({ /* Lottie animation configuration */ });
function handleExcelButtonClick(){
    // Send a request to the Flask route using JavaScript
    fetch('/run_code', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => console.log(data)) // Log any response from the server
    .catch(error => console.error('Error:',error));
}