// Simple endpoint to check deployment structure
const fs = require('fs');
const path = require('path');

// Vercel serverless function format
export default function handler(req, res) {
  // Report on the file structure to help diagnose issues
  const results = {
    status: 'ok',
    check_time: new Date().toISOString(),
    current_directory: process.cwd(),
    deployment_structure: {}
  };

  // Check if frontend directory exists
  try {
    const frontendPath = path.join(process.cwd(), 'frontend');
    if (fs.existsSync(frontendPath)) {
      results.deployment_structure.frontend = {
        exists: true,
        contents: fs.readdirSync(frontendPath)
      };

      // Check for frontend/build
      const buildPath = path.join(frontendPath, 'build');
      if (fs.existsSync(buildPath)) {
        results.deployment_structure.frontend.build = {
          exists: true,
          contents: fs.readdirSync(buildPath)
        };

        // Check for index.html in build
        const indexPath = path.join(buildPath, 'index.html');
        if (fs.existsSync(indexPath)) {
          results.deployment_structure.frontend.build.index_exists = true;
        } else {
          results.deployment_structure.frontend.build.index_exists = false;
        }
      } else {
        results.deployment_structure.frontend.build = {
          exists: false
        };
      }
    } else {
      results.deployment_structure.frontend = {
        exists: false
      };
    }
  } catch (error) {
    results.deployment_structure.frontend_error = error.message;
  }

  // Check for root index.html
  try {
    const rootIndexPath = path.join(process.cwd(), 'index.html');
    results.deployment_structure.root_index_exists = fs.existsSync(rootIndexPath);
  } catch (error) {
    results.deployment_structure.root_index_error = error.message;
  }

  // List root directory
  try {
    results.deployment_structure.root_contents = fs.readdirSync(process.cwd());
  } catch (error) {
    results.deployment_structure.root_error = error.message;
  }

  // Get vercel.json content
  try {
    const vercelJsonPath = path.join(process.cwd(), 'vercel.json');
    if (fs.existsSync(vercelJsonPath)) {
      results.deployment_structure.vercel_json = JSON.parse(fs.readFileSync(vercelJsonPath, 'utf8'));
    }
  } catch (error) {
    results.deployment_structure.vercel_json_error = error.message;
  }

  // Environment info
  results.environment = {
    NODE_ENV: process.env.NODE_ENV,
    VERCEL_ENV: process.env.VERCEL_ENV,
    VERCEL_REGION: process.env.VERCEL_REGION
  };

  res.status(200).json(results);
} 