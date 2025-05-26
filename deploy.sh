#!/bin/bash

# House Hunt Challenge - Deployment Preparation Script
echo "🚀 Preparing House Hunt Challenge for deployment..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Create production environment file for frontend
echo "📝 Creating production environment file..."
cd frontend
echo "REACT_APP_API_URL=https://your-backend-url.railway.app" > .env.production
echo "GENERATE_SOURCEMAP=false" >> .env.production
echo "✅ Created frontend/.env.production"

# Go back to root
cd ..

# Check if all deployment files exist
echo "🔍 Checking deployment files..."
files=("railway.json" "Procfile" "requirements.txt" "DEPLOYMENT.md" "frontend/vercel.json")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

echo ""
echo "🎯 Next Steps:"
echo "1. Update frontend/.env.production with your actual Railway URL"
echo "2. Update main.py CORS configuration with your actual Vercel URL"
echo "3. Push to GitHub: git add . && git commit -m 'Prepare for deployment' && git push"
echo "4. Follow the DEPLOYMENT.md guide"
echo ""
echo "📚 Read DEPLOYMENT.md for complete instructions"
echo "🚀 Happy deploying!" 