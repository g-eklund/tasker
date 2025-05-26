# 🚀 Deployment Guide: House Hunt Challenge

## Overview
This guide will help you deploy the House Hunt Challenge app using:
- **Backend**: Railway (FastAPI + Supabase)
- **Frontend**: Vercel (React)

## 📋 Prerequisites
- GitHub account
- Railway account (free tier available)
- Vercel account (free tier available)
- Supabase project with your database

---

## 🛤️ Part 1: Deploy Backend to Railway

### Step 1: Prepare Your Repository
1. Push your code to GitHub
2. Ensure all files are committed including:
   - `railway.json`
   - `Procfile`
   - `requirements.txt`
   - `main.py` (with production updates)

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect it's a Python project

### Step 3: Configure Environment Variables
In Railway dashboard, go to Variables tab and add:

```bash
# Required Environment Variables
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
HOST=0.0.0.0
PORT=8000
FRONTEND_URL=https://your-app-name.vercel.app
```

### Step 4: Update CORS Configuration
1. After deployment, note your Railway app URL (e.g., `https://your-app-name.railway.app`)
2. Update the CORS configuration in `main.py`:
   ```python
   allowed_origins = [
       "http://localhost:3000",
       "https://*.vercel.app",
       "https://your-actual-frontend-domain.vercel.app",  # Update this
   ]
   ```

### Step 5: Test Backend
- Visit your Railway URL
- You should see the FastAPI docs at `/docs`

---

## ⚡ Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend
1. Navigate to the `frontend` directory
2. Create production environment variables:
   ```bash
   # In frontend directory, create .env.production
   echo "REACT_APP_API_URL=https://your-backend-url.railway.app" > .env.production
   echo "GENERATE_SOURCEMAP=false" >> .env.production
   ```

### Step 2: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Set **Root Directory** to `frontend`
6. Vercel will auto-detect it's a React app

### Step 3: Configure Environment Variables
In Vercel dashboard, go to Settings → Environment Variables:

```bash
REACT_APP_API_URL=https://your-backend-url.railway.app
GENERATE_SOURCEMAP=false
```

### Step 4: Update Backend CORS
1. Note your Vercel URL (e.g., `https://house-hunt-challenge.vercel.app`)
2. Update Railway environment variable:
   ```bash
   FRONTEND_URL=https://your-vercel-url.vercel.app
   ```

---

## 🔧 Alternative Deployment Options

### Option 1: Render (Backend Alternative)
- Similar to Railway
- Good free tier
- Auto-deploys from GitHub

### Option 2: Netlify (Frontend Alternative)
- Similar to Vercel
- Great for static sites
- Built-in form handling

### Option 3: DigitalOcean App Platform
- Can host both frontend and backend
- More traditional cloud approach
- Good for larger applications

---

## 🌍 Production Checklist

### Backend (Railway)
- [ ] Environment variables configured
- [ ] CORS origins updated
- [ ] Supabase connection working
- [ ] API endpoints responding
- [ ] Health check passing

### Frontend (Vercel)
- [ ] Build successful
- [ ] Environment variables set
- [ ] API calls working
- [ ] Camera permissions working
- [ ] All routes accessible

### Security
- [ ] Remove debug mode in production
- [ ] Secure API keys
- [ ] HTTPS enabled (automatic with Railway/Vercel)
- [ ] CORS properly configured

---

## 🚨 Troubleshooting

### Common Issues

**Backend not starting:**
- Check Railway logs for Python errors
- Verify all dependencies in requirements.txt
- Ensure PORT environment variable is set

**Frontend can't connect to backend:**
- Verify REACT_APP_API_URL is correct
- Check CORS configuration
- Ensure backend is running

**Camera not working:**
- HTTPS is required for camera access
- Both Railway and Vercel provide HTTPS automatically

**Build failures:**
- Check Node.js version compatibility
- Verify all dependencies are installed
- Review build logs for specific errors

---

## 💰 Cost Estimates

### Free Tier Limits
- **Railway**: 500 hours/month, $5 credit
- **Vercel**: 100GB bandwidth, unlimited deployments
- **Supabase**: 500MB database, 2GB bandwidth

### Scaling Costs
- **Railway**: ~$5-20/month for small apps
- **Vercel**: ~$20/month for Pro features
- **Total**: ~$25-40/month for production app

---

## 🎯 Next Steps

1. **Custom Domain**: Add your own domain in Vercel
2. **Analytics**: Add Vercel Analytics or Google Analytics
3. **Monitoring**: Set up error tracking (Sentry)
4. **CI/CD**: Automatic deployments on git push
5. **Performance**: Add caching and optimization

---

## 📞 Support

If you encounter issues:
1. Check the deployment logs
2. Verify environment variables
3. Test API endpoints manually
4. Check CORS configuration
5. Review this guide step-by-step

Happy deploying! 🚀 