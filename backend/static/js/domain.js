document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.getElementById("submitBtn");
  const showAllBtn = document.getElementById("showAllBtn");
  const exportBtn = document.getElementById("exportExcelBtn");
  const fileInput = document.getElementById("fileInput");
  const resultsTable = document.getElementById("resultsTable");
  const pagination = document.getElementById("pagination");
  const PAGE_SIZE = 25;
  let currentPage = 1;

  // === Загальна функція для запиту та відображення ===
  async function fetchResults(url, page = 1) {
    const offset = (page - 1) * PAGE_SIZE;

    resultsTable.innerHTML = `
      <tr>
        <td colspan="3" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Завантаження...</span>
          </div>
        </td>
      </tr>
    `;

    try {
      const response = await fetch(`${url}${url.includes("?") ? "&" : "?"}limit=${PAGE_SIZE}&offset=${offset}`);
      if (response.status === 404) {
        resultsTable.innerHTML = `
          <tr><td colspan="3" class="text-center text-muted">Дані відсутні</td></tr>
        `;
        pagination.innerHTML = "";
        return;
      }

      if (!response.ok) throw new Error("Помилка при отриманні даних");
      const data = await response.json();

      renderResults(data);
      renderPagination(data.length, page, url);
    } catch (error) {
      resultsTable.innerHTML = `
        <tr><td colspan="3" class="text-danger text-center">Не вдалося отримати дані</td></tr>
      `;
      pagination.innerHTML = "";
    }
  }

  // === Відображення таблиці ===
  function renderResults(data) {
    resultsTable.innerHTML = "";
    if (!data || data.length === 0) {
      resultsTable.innerHTML = `<tr><td colspan="3" class="text-center text-muted">Немає записів</td></tr>`;
      return;
    }

    data.forEach(item => {
      const row = `<tr>
        <td>${item.domain_name || "-"}</td>
        <td>${item.ip_address || "-"}</td>
        <td>${item.block_list || "-"}</td>
      </tr>`;
      resultsTable.insertAdjacentHTML("beforeend", row);
    });
  }

  // === Пагінація ===
  function renderPagination(itemsCount, page, url) {
    pagination.innerHTML = "";

    const prevLi = document.createElement("li");
    prevLi.className = `page-item ${page === 1 ? "disabled" : ""}`;
    prevLi.innerHTML = `<a class="page-link" href="#">Попередня</a>`;
    prevLi.addEventListener("click", (e) => {
      e.preventDefault();
      if (page > 1) {
        currentPage--;
        fetchResults(url, currentPage);
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
        fetchResults(url, currentPage);
      }
    });
    pagination.appendChild(nextLi);
  }

  // === Події ===
  searchBtn.addEventListener("click", async () => {
    const domain = document.getElementById("inputValue").value.trim();
    if (!domain) return alert("Введіть домен або IP для пошуку!");
    currentPage = 1;
    await fetchResults(`/domain/search?domain=${encodeURIComponent(domain)}`);
  });

  showAllBtn.addEventListener("click", async () => {
    currentPage = 1;
    await fetchResults("/domain/list");
  });

  fileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    alert("Функціонал у розробці");
    return;
    // const formData = new FormData();
    // formData.append("file", file);
    //
    // const res = await fetch("/domain/upload", { method: "POST", body: formData });
    // if (!res.ok) return alert("Помилка при завантаженні файлу!");
    // const data = await res.json();
    // renderResults(data);
  });

  exportBtn.addEventListener("click", async () => {
    const response = await fetch("/domain/excel-export");
    if (!response.ok) return alert("Помилка при експорті!");
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    const disposition = response.headers.get("Content-Disposition");
    const filename = disposition.match(/filename="?([^"]+)"?/);
    a.href = url;
    a.download = filename[1];
    a.click();
  });

  // === Автоматично показати всі записи ===
  fetchResults("/domain/list");
});
