const { createServer } = require('http');
const { parse } = require('url');
const fs = require('fs');
const path = require('path');

// 简单模拟 Flask 请求处理
createServer((req, res) => {
  const url = parse(req.url, true);
  if (url.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message: 'Performance Report Analyzer is running on Vercel!' }));
  } else if (url.pathname === '/api/analyze') {
    // 模拟文件上传逻辑（实际需要更复杂处理）
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ summary: 'Demo mode: file received', issues: [] }));
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  }
}).listen(process.env.PORT || 3000);
