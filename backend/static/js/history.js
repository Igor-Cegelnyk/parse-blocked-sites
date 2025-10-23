document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("historyTable");
  const pagination = document.getElementById("pagination");
  const manualLoadBtn = document.getElementById("manualLoadBtn");
  const blockListSelect = document.getElementById("blockListSelect");
  const PAGE_SIZE = 25;
  let currentPage = 1;

  async function fetchHistory(page = 2) {
    const offset = (page - 1) * PAGE_SIZE;

    tableBody.innerHTML = `
      <tr>
        <td colspan="6" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Завантаження...</span>
          </div>
        </td>
      </tr>
    `;

    try {
      const response = await fetch(`/history/log?limit=${PAGE_SIZE}&offset=${offset}`);
      if (!response.ok) throw new Error("Помилка при завантаженні історії");

      const logs = await response.json(); // масив записів

      tableBody.innerHTML = "";

      if (logs.length === 0) {
        tableBody.innerHTML = `
          <tr>
            <td colspan="6" class="text-center text-muted">Немає записів</td>
          </tr>`;
        pagination.innerHTML = "";
        return;
      }

      logs.forEach(log => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${log.created_date}</td>
          <td>${log.created_time}</td>
          <td>${log.block_list}</td>
          <td>${log.parse_domain_quantity}</td>
          <td>${log.new_domain_quantity}</td>
          <td>${log.remove_domain_quantity}</td>
          <td>${log.log_status}</td>
        `;
        tableBody.appendChild(row);
      });

      renderPagination(logs.length, page);
    } catch (error) {
      console.error(error);
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" class="text-danger text-center">Не вдалося отримати дані</td>
        </tr>`;
      pagination.innerHTML = "";
    }
  }

  function renderPagination(itemsCount, page) {
    pagination.innerHTML = "";

    // Попередня
    const prevLi = document.createElement("li");
    prevLi.className = `page-item ${page === 1 ? "disabled" : ""}`;
    prevLi.innerHTML = `<a class="page-link" href="#">Попередня</a>`;
    prevLi.addEventListener("click", (e) => {
      e.preventDefault();
      if (page > 1) {
        currentPage--;
        fetchHistory(currentPage);
      }
    });
    pagination.appendChild(prevLi);

    // Наступна
    const nextLi = document.createElement("li");
    nextLi.className = `page-item ${itemsCount < PAGE_SIZE ? "disabled" : ""}`;
    nextLi.innerHTML = `<a class="page-link" href="#">Наступна</a>`;
    nextLi.addEventListener("click", (e) => {
      e.preventDefault();
      if (itemsCount === PAGE_SIZE) {
        currentPage++;
        fetchHistory(currentPage);
      }
    });
    pagination.appendChild(nextLi);
  }

  manualLoadBtn.addEventListener("click", async () => {
    manualLoadBtn.disabled = true;
    manualLoadBtn.textContent = "Завантаження...";

    const selectedBlockList = blockListSelect.value;

    try {
      const response = await fetch("/history/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ block_list: selectedBlockList }),
      });
      if (!response.ok) throw new Error("Помилка при ручному завантаженні");

    } catch (err) {
      alert("Не вдалося виконати ручне завантаження");
      // console.error(err);
    } finally {
      manualLoadBtn.disabled = false;
      manualLoadBtn.textContent = "Ручне завантаження";
      fetchHistory(currentPage);
    }
  });

  // Початкове завантаження
  fetchHistory(currentPage);
});
