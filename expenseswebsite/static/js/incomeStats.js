const renderIncomeChart = (data, labels) => {
  const ctx = document.getElementById("incomeChart").getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [{
        label: "Last 6 Months Income",
        data: data,
        backgroundColor: [
          "rgba(54, 162, 235, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(231, 233, 237, 0.2)"
        ],
        borderColor: [
          "rgba(54, 162, 235, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(200, 200, 200, 1)"
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Income per Source"
        }
      }
    }
  });
};

const getIncomeData = () => {
  fetch("/income/income_category_summary")
    .then((res) => res.json())
    .then((results) => {
      const data = results.income_category_data;
      const labels = Object.keys(data);
      const values = Object.values(data);

      renderIncomeChart(values, labels);
    });
};

document.addEventListener("DOMContentLoaded", getIncomeData);
