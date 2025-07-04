document.addEventListener('DOMContentLoaded', () => {
    const searchField = document.getElementById('searchField');
    const defaultTable = document.querySelector('.app-table');
    const tableOutput = document.querySelector('.table-output');
    const tableBody = document.querySelector('.table-body');
    const noResults = document.querySelector('.no-results');
    const pagination = document.querySelector('.pagination-container');
  
    const csrfToken = getCookie('csrftoken');
  
    searchField.addEventListener('keyup', (e) => {
      const searchValue = e.target.value.trim();
  
      if (searchValue.length > 0) {
        fetch('/income/search-income', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({ searchText: searchValue })
        })
        .then(res => res.json())
        .then(data => {
          pagination.style.display = 'none';
          tableBody.innerHTML = '';
  
          if (data.length === 0) {
            tableOutput.style.display = 'none';
            noResults.style.display = 'block';
          } else {
            noResults.style.display = 'none';
            defaultTable.style.display = 'none';
            tableOutput.style.display = 'block';
  
            data.forEach(item => {
              const row = `
                <tr>
                  <td>${item.amount}</td>
                  <td>${item.source}</td>
                  <td>${item.description}</td>
                  <td>${item.date}</td>
                  <td>
                    <a href="/income/edit-income/${item.id}" class="btn btn-secondary btn-sm">Edit</a>
                  </td>
                </tr>
              `;
              tableBody.innerHTML += row;
            });
          }
        });
      } else {
        // Reset view
        noResults.style.display = 'none';
        tableOutput.style.display = 'none';
        defaultTable.style.display = 'block';
        pagination.style.display = 'block';
      }
    });
  
    // Helper function to get CSRF token from cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  