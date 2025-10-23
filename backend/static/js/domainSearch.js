$(document).ready(function() {
  $("#submitBtn").off("click").on("click", function() {
    const domain = $("#inputValue").val().trim();

    // Якщо поле порожнє — показуємо повідомлення і виходимо
    if (!domain) {
      alert("Будь ласка, введіть домен або IP адресу!");
      return;
    }

    // Очищаємо таблицю перед новим пошуком
    $("#resultsTable").empty();

    $.ajax({
      url: "/domain-search/search",
      type: "GET",
      data: { domain: domain },
      beforeSend: function() {
        $("#resultsTable").append(`
          <tr id="loadingRow">
            <td colspan="3" class="text-center text-muted">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Завантаження...</span>
              </div>
            </td>
          </tr>
        `);
      },
      success: function(data) {
        $("#loadingRow").remove();

        if (!data || data.length === 0) {
          $("#resultsTable").append(`
            <tr>
              <td colspan="3" class="text-center text-muted">Нічого не знайдено</td>
            </tr>
          `);
          return;
        }

        data.forEach(item => {
          $("#resultsTable").append(`
            <tr>
              <td>${item.domain_name || "-"}</td>
              <td>${item.ip_address || "-"}</td>
              <td>${item.block_list || "-"}</td>
            </tr>
          `);
        });

        $("#inputValue").val("");
      },
      error: function(xhr) {
        $("#loadingRow").remove();
        console.error(xhr.responseText);
        alert("Сталася помилка при отриманні даних.");
      }
    });
  });
});
