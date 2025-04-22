document.addEventListener('DOMContentLoaded', () => {
    const eventSelect = document.getElementById('event-select');
    const generateButton = document.getElementById('generate-fake-data');
    let chartInstance = null;

    // 填充下拉框
    async function loadEvents() {
        try {
            const response = await fetch('/api/monitor/events');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Events API response:', data);
            eventSelect.innerHTML = '<option value="">-- Select an Event --</option>';
            if (data.events && data.events.length > 0) {
                data.events.forEach(event => {
                    const option = document.createElement('option');
                    option.value = event.id; // 使用 event_id
                    option.textContent = event.name; // 显示 event_name
                    eventSelect.appendChild(option);
                });
            } else {
                console.warn('No events found in API response');
                alert('No events available. Please generate fake data.');
            }
        } catch (error) {
            console.error('Error loading events:', error);
            alert('Failed to load events: ' + error.message);
        }
    }

    // 渲染图表
    async function renderChart(eventId) {
        try {
            const response = await fetch(`/api/monitor/trend/${eventId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Trend API response:', data);

            if (!data.dates || data.dates.length === 0) {
                alert(`No trend data available for event ID ${eventId}`);
                return;
            }

            // 销毁现有图表
            if (chartInstance) {
                chartInstance.destroy();
            }

            // 获取事件名称（从下拉框的显示文本）
            const eventName = eventSelect.selectedOptions[0].textContent;
            const ctx = document.getElementById('sentiment-chart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [
                        {
                            label: 'Positive (%)',
                            data: data.positive,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            fill: true
                        },
                        {
                            label: 'Negative (%)',
                            data: data.negative,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: { display: true, text: 'Percentage (%)' }
                        },
                        x: { title: { display: true, text: 'Date' } }
                    },
                    plugins: {
                        legend: { display: true },
                        title: { display: true, text: `Sentiment Trend for ${eventName}` },
                        tooltip: {
                            callbacks: {
                                label: (context) => `${context.dataset.label}: ${context.parsed.y.toFixed(1)}%`
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error rendering chart:', error);
            alert('Failed to load chart data: ' + error.message);
        }
    }

    // 生成假数据
    async function generateFakeData() {
        try {
            const response = await fetch('/api/generate_fake_data', { method: 'POST' });
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                loadEvents();
                if (eventSelect.options.length > 1) {
                    eventSelect.value = eventSelect.options[1].value;
                    renderChart(eventSelect.value);
                }
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error generating fake data:', error);
            alert('Failed to generate fake data: ' + error.message);
        }
    }

    // 事件监听
    eventSelect.addEventListener('change', (e) => {
        const eventId = e.target.value;
        if (eventId) {
            renderChart(eventId);
        }
    });

    generateButton.addEventListener('click', generateFakeData);

    // 初始加载事件
    loadEvents();
});