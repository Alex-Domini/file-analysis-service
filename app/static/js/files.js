let currentPage = 1;
const pageSize = 10;

const selectedFileIds = new Set();

const statisticsSection =
    document.getElementById("statisticsSection");

const totalStatisticsBody =
    document.getElementById("totalStatisticsBody");

const fileStatistics =
    document.getElementById("fileStatistics");

const tableBody =
    document.getElementById("filesTableBody");

const previousButton =
    document.getElementById("previousPageButton");

const nextButton =
    document.getElementById("nextPageButton");

const paginationInfo =
    document.getElementById("paginationInfo");

const selectPageCheckbox =
    document.getElementById("selectPageCheckbox");

const selectAllCheckbox =
    document.getElementById("selectAllCheckbox");

const calculateButton =
    document.getElementById("calculateButton");


function getFileCheckboxes() {
    return document.querySelectorAll(".file-checkbox");
}


async function loadFiles(page = 1) {
    try {
        const response = await fetch(
            `/files?page=${page}&page_size=${pageSize}`
        );

        if (!response.ok) {
            throw new Error(
                `Ошибка загрузки файлов: ${response.status}`
            );
        }

        const data = await response.json();

        renderTable(data.items);
        updatePagination(data.pagination);

        currentPage = page;
    } catch (error) {
        console.error(error);
        alert("Не удалось загрузить список файлов");
    }
}

function renderCurrentPageSelection() {
    const checkboxes = getFileCheckboxes();

    for (const checkbox of checkboxes) {
        const fileId = Number(checkbox.value);

        checkbox.checked = selectedFileIds.has(fileId);
    }

    updateSelectPageCheckbox();
}


function renderTable(files) {
    tableBody.innerHTML = "";

    if (files.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="3" class="empty-message">
                    Скачанных файлов пока нет
                </td>
            </tr>
        `;

        selectPageCheckbox.checked = false;
        selectPageCheckbox.indeterminate = false;

        return;
    }

    for (const file of files) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <input
                    type="checkbox"
                    value="${file.id}"
                    class="file-checkbox"
                    ${selectedFileIds.has(file.id) ? "checked" : ""}
                >
            </td>

            <td>${file.filename}</td>

            <td>
                ${new Date(file.downloaded_at)
                    .toLocaleString("ru-RU")}
            </td>
        `;

        tableBody.appendChild(row);
    }

    addFileCheckboxListeners();
    updateSelectPageCheckbox();
}


function addFileCheckboxListeners() {
    const checkboxes = getFileCheckboxes();

    for (const checkbox of checkboxes) {
        checkbox.addEventListener("change", () => {
            const fileId = Number(checkbox.value);

            if (checkbox.checked) {
                selectedFileIds.add(fileId);
            } else {
                selectedFileIds.delete(fileId);
            }

            updateSelectPageCheckbox();
        });
    }
}


function updateSelectPageCheckbox() {
    const checkboxes = Array.from(getFileCheckboxes());

    if (checkboxes.length === 0) {
        selectPageCheckbox.checked = false;
        selectPageCheckbox.indeterminate = false;
        return;
    }

    const selectedCount = checkboxes.filter(
        (checkbox) => checkbox.checked
    ).length;

    selectPageCheckbox.checked =
        selectedCount === checkboxes.length;

    selectPageCheckbox.indeterminate =
        selectedCount > 0 &&
        selectedCount < checkboxes.length;
}


function updatePagination(pagination) {
    const totalPages = pagination.total_pages;

    paginationInfo.textContent =
        totalPages === 0
            ? "Страница 0 из 0"
            : `Страница ${pagination.page} из ${totalPages}`;

    previousButton.disabled =
        pagination.page <= 1;

    nextButton.disabled =
        totalPages === 0 ||
        pagination.page >= totalPages;
}


function renderStatistics(data) {
    statisticsSection.hidden = false;

    renderTotalStatistics(data.total);
    renderFileStatistics(data.files);

    statisticsSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });
}


function renderTotalStatistics(total) {
    totalStatisticsBody.innerHTML = "";

    for (let digit = 0; digit <= 9; digit++) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${digit}</td>
            <td>${total[digit] ?? 0}</td>
        `;

        totalStatisticsBody.appendChild(row);
    }
}


function renderFileStatistics(files) {
    fileStatistics.innerHTML = "";

    for (const file of files) {
        const card = document.createElement("div");

        card.className = "file-statistics-card";

        let rows = "";

        for (let digit = 0; digit <= 9; digit++) {
            rows += `
                <tr>
                    <td>${digit}</td>
                    <td>${file.digits[digit] ?? 0}</td>
                </tr>
            `;
        }

        card.innerHTML = `
            <h3>${file.filename}</h3>

            <table>
                <thead>
                    <tr>
                        <th>Цифра</th>
                        <th>Количество</th>
                    </tr>
                </thead>

                <tbody>
                    ${rows}
                </tbody>
            </table>
        `;

        fileStatistics.appendChild(card);
    }
}


selectPageCheckbox.addEventListener("change", () => {
    const checkboxes = getFileCheckboxes();

    for (const checkbox of checkboxes) {
        const fileId = Number(checkbox.value);

        checkbox.checked = selectPageCheckbox.checked;

        if (selectPageCheckbox.checked) {
            selectedFileIds.add(fileId);
        } else {
            selectedFileIds.delete(fileId);
        }
    }

    selectPageCheckbox.indeterminate = false;
});


selectAllCheckbox.addEventListener("change", async () => {
    selectAllCheckbox.disabled = true;

    try {
        if (selectAllCheckbox.checked) {
            const response = await fetch("/files/ids");

            if (!response.ok) {
                throw new Error(
                    `Не удалось получить ID файлов: ${response.status}`
                );
            }

            const data = await response.json();

            selectedFileIds.clear();

            for (const id of data.ids) {
                selectedFileIds.add(Number(id));
            }
        } else {
            selectedFileIds.clear();
        }

        renderCurrentPageSelection();
    } catch (error) {
        console.error(error);

        selectAllCheckbox.checked = false;

        alert(`Ошибка выбора файлов: ${error.message}`);
    } finally {
        selectAllCheckbox.disabled = false;
    }
});


previousButton.addEventListener("click", () => {
    if (currentPage > 1) {
        loadFiles(currentPage - 1);
    }
});


nextButton.addEventListener("click", () => {
    loadFiles(currentPage + 1);
});


calculateButton.addEventListener("click", async () => {
    const selectedIds = Array.from(selectedFileIds);

    if (selectedIds.length === 0) {
        alert("Выберите хотя бы один файл");
        return;
    }

    calculateButton.disabled = true;
    calculateButton.textContent = "Выполняется расчёт...";

    try {
        const response = await fetch("/files/statistics", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                file_ids: selectedIds,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail)
            );
        }

        renderStatistics(data);
    } catch (error) {
        console.error(error);
        alert(`Ошибка расчёта: ${error.message}`);
    } finally {
        calculateButton.disabled = false;
        calculateButton.textContent = "Произвести расчёты";
    }
});


loadFiles();