document.addEventListener('DOMContentLoaded', function () {
  const chartDom = document.getElementById('metric-chart');
  const myChart = echarts.init(chartDom);

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
      data: ['Precision', 'Recall', 'F1-score']
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 1
    },
    series: [
      {
        name: 'Naive Bayes',
        type: 'bar',
        data: [0.900, 0.917, 0.899]
      },
      {
        name: 'Logistic Regression',
        type: 'bar',
        data: [0.929, 0.875, 0.890]
      }
    ]
  };

  myChart.setOption(option);
});