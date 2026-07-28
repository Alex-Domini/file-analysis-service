const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");

const statusElement = document.getElementById("status");
const startedAtElement = document.getElementById("startedAt");
const currentBatchElement = document.getElementById("currentBatch");
const downloadedCountElement = document.getElementById("downloadedCount");
const errorElement = document.getElementById("error");

let statusInterval = null;


function startPolling() {
    if (statusInterval !== null) {
        return;
    }

    statusInterval = setInterval(loadStatus, 1000);
}


function stopPolling() {
    if (statusInterval === null) {
        return;
    }

    clearInterval(statusInterval);
    statusInterval = null;
}


async function startDownload() {
    const response = await fetch("/download", {
        method: "POST",
    });

    if (!response.ok) {
        const data = await response.json();
        alert(data.detail ?? "Не удалось начать загрузку");
        return;
    }

    await loadStatus();
    startPolling();
}


async function stopDownload() {
    const response = await fetch("/download/stop", {
        method: "POST",
    });

    if (!response.ok) {
        const data = await response.json();
        alert(data.detail ?? "Не удалось остановить загрузку");
        return;
    }

    await loadStatus();
}


async function loadStatus() {
    const response = await fetch("/download/status");

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    statusElement.textContent = data.status;
    if (data.started_at) {
    const date = new Date(data.started_at);

    startedAtElement.textContent = date.toLocaleString("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });
} else {
    startedAtElement.textContent = "—";
}
    downloadedCountElement.textContent = data.downloaded_count ?? 0;
    
    if (data.current_batch_total > 0) {
    currentBatchElement.textContent =
        `Получено ${data.current_batch_total} названий файлов, ` +
        `скачано ${data.current_batch_downloaded} из ${data.current_batch_total}`;
    } else {
        currentBatchElement.textContent = "—";
    }


    errorElement.textContent = data.error ?? "—";

    const isRunning = data.status === "running";

    startButton.disabled = isRunning;
    stopButton.disabled = !isRunning;

    if (isRunning) {
        startPolling();
    } else {
        stopPolling();
    }
}


startButton.addEventListener("click", startDownload);
stopButton.addEventListener("click", stopDownload);

loadStatus();