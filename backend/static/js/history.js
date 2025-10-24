document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("historyTable");
  const pagination = document.getElementById("pagination");
  const manualLoadBtn = document.getElementById("manualLoadBtn");
  const blockListSelect = document.getElementById("blockListSelect");
  const statusSelect = document.getElementById("statusSelect");
  const showBtn = document.getElementById("showBtn");
  const PAGE_SIZE = 25;
  let currentPage = 1;

  async function fetchHistory(page = 1) {
    const offset = (page - 1) * PAGE_SIZE;
    const blockList = blockListSelect.value;
    const status = statusSelect.value;

    tableBody.innerHTML = `
      <tr>
        <td colspan="7" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Завантаження...</span>
          </div>
        </td>
      </tr>
    `;

    const queryParams = new URLSearchParams({
      limit: PAGE_SIZE,
      offset,
    });
    if (blockList) queryParams.append("block_list", blockList);
    if (status) queryParams.append("log_status", status);

    try {
      const response = await fetch(`/history/log?${queryParams.toString()}`);
      if (response.status === 404) {
        tableBody.innerHTML = `
          <tr>
            <td colspan="7" class="text-center text-muted">Немає записів</td>
          </tr>`;
        pagination.innerHTML = "";
        return;
      }
      if (!response.ok) throw new Error("Помилка при завантаженні історії");

      const logs = await response.json();
      tableBody.innerHTML = "";

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
      tableBody.innerHTML = `
        <tr>
          <td colspan="7" class="text-danger text-center">Не вдалося отримати дані</td>
        </tr>`;
      pagination.innerHTML = "";
    }
  }

  function renderPagination(itemsCount, page) {
    pagination.innerHTML = "";

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
    const selectedBlockList = blockListSelect.value;

    if (!selectedBlockList) {
      alert("Оберіть список блокування перед завантаженням");
      return;
    }

    manualLoadBtn.disabled = true;
    manualLoadBtn.textContent = "Завантаження...";

    try {
      const response = await fetch("/history/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ block_list: selectedBlockList }),
      });
      if (!response.ok) throw new Error("Помилка при ручному завантаженні");
    } catch (err) {
      alert("Не вдалося виконати ручне завантаження");
    } finally {
      manualLoadBtn.disabled = false;
      manualLoadBtn.textContent = "Ручне завантаження";
      fetchHistory(currentPage);
    }
  });

  showBtn.addEventListener("click", () => {
    currentPage = 1;
    fetchHistory(currentPage);
  });

  fetchHistory(currentPage);
});
