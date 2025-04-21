function analyze() {
  const text = document.getElementById("inputText").value;
  if (!text.trim()) {
    alert("请输入文本内容！");
    return;
  }

  fetch('/api/analysis/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  })
    .then(res => res.json())
    .then(data => {
      const box = document.getElementById("resultText");
      if (data.sentiment) {
        box.innerText = `情感判断结果：${data.sentiment.toUpperCase()}（代码：${data.code}）`;
        if (data.probabilities) {
          const probText = `\n置信度：\nNEGATIVE: ${data.probabilities.negative}%\nPOSITIVE: ${data.probabilities.positive}%`;
          box.innerText += probText;
        }
      } else {
        box.innerText = `错误：${data.error || "未知错误"}`;
      }
    })
    .catch(err => {
      document.getElementById("resultText").innerText = "请求失败：" + err;
    });
}