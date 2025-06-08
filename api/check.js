// Simple endpoint to check deployment structure
const fs = require('fs');
const path = require('path');

export default function handler(req, res) {
  try {
    // List of directories to check
    const dirsToCheck = [
      '/',
      '/frontend',
      '/frontend/build',
      '/frontend/build/static'
    ];
    
    // Check if directories exist
    const results = {};
    for (const dir of dirsToCheck) {
      const fullPath = path.join(process.cwd(), dir);
      try {
        const exists = fs.existsSync(fullPath);
        const files = exists ? fs.readdirSync(fullPath) : [];
        results[dir] = {
          exists,
          files: files.slice(0, 10) // Show up to 10 files
        };
      } catch (e) {
        results[dir] = { exists: false, error: e.message };
      }
    }

    // Check for index.html specifically
    const indexPath = path.join(process.cwd(), '/frontend/build/index.html');
    const indexExists = fs.existsSync(indexPath);
    
    return res.status(200).json({
      directories: results,
      indexHtml: indexExists,
      currentDirectory: process.cwd(),
      env: {
        NODE_ENV: process.env.NODE_ENV,
        VERCEL_ENV: process.env.VERCEL_ENV
      }
    });
  } catch (error) {
    return res.status(500).json({
      error: error.message,
      stack: error.stack
    });
  }
} 