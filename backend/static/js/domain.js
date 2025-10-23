document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("domainTable");
  const pagination = document.getElementById("pagination");
  const exportExcelBtn = document.getElementById("exportExcelBtn");
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
      const response = await fetch(`/domain/all?limit=${PAGE_SIZE}&offset=${offset}`);
      if (!response.ok) throw new Error("Помилка при завантаженні даних");

      const domains = await response.json();

      tableBody.innerHTML = "";

      if (domains.length === 0) {
        tableBody.innerHTML = `
          <tr>
            <td colspan="6" class="text-center text-muted">Немає записів</td>
          </tr>`;
        pagination.innerHTML = "";
        return;
      }

      domains.forEach(domain => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${domain.domain_name || "-"}</td>
          <td>${domain.ip_address || "-"}</td>
          <td>${domain.block_list || "-"}</td>
        `;
        tableBody.appendChild(row);
      });

      renderPagination(domains.length, page);
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

  exportExcelBtn.addEventListener("click", async () => {
  exportExcelBtn.disabled = true;
  exportExcelBtn.textContent = "Готуємо файл...";

  try {
        const response = await fetch("/domain/excel-export", { method: "GET" });
        if (!response.ok) throw new Error("Помилка при експортуванні в Excel");

        const disposition = response.headers.get("Content-Disposition");
        const match = disposition.match(/filename="?([^"]+)"?/);

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = match[1];
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

      } catch (err) {
        alert("Не вдалося завантажити Excel файл");
        console.error(err);
      } finally {
        exportExcelBtn.disabled = false;
        exportExcelBtn.textContent = "Експорт в Excel";
      }
  });

  fetchHistory(currentPage);
});
