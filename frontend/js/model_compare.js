console.log("✅ model_compare.js loaded");
document.addEventListener('DOMContentLoaded', function () {
  const chartDom = document.getElementById('metric-chart');
  const myChart = echarts.init(chartDom);

  fetch('/api/monitor/model_metrics')
    .then(response => response.json())
    .then(data => {
      const metricLabels = data.metrics; // ['Precision', 'Recall', 'F1-score']
      const seriesData = [];

      for (const key in data) {
        if (key !== 'metrics') {
          seriesData.push({
            name: key,
            type: 'bar',
            data: data[key]
          });
        }
      }

      const option = {
        title: {
          text: '模型宏平均性能对比',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          top: 'bottom'
        },
        xAxis: {
          type: 'category',
          data: metricLabels
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 1
        },
        series: seriesData
      };

      myChart.setOption(option);
    })
    .catch(error => {
      console.error("获取模型评估数据失败：", error);
    });
});